from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from dataSource.usersBase import usersBase
from dataSource.movsUsersBase import movsBase
from time import time
import pandas as pd
from pandas import ExcelWriter
from PyPDF2 import PdfWriter, PdfReader
from typing import List, Tuple
import os

def cuentaInter() -> list:
    """
        CuentaInter recupera el numero de cuentas Interbancarias de un archivo excel.
    Returns:
        Lista con los objetos de las cuentas junto con Nit y la cuenta coovitel.
    """
    try:
        # Intenta leer el archivo Excel
        df = pd.read_excel("dataSource/cuentasInter.xlsx")
        
        # Verifica si las columnas existen en el DataFrame
        columns = ['documento', 'CuentaCoovitel', 'Cuenta Interbancaria']
        if not all(column in df.columns for column in columns):
            print("Algunas columnas no existen en el archivo Excel.")
            return []
        
        # Selecciona solo algunas columnas
        df_selected = df[columns]
        
        # Convierte el DataFrame seleccionado en una lista de diccionarios
        listDates = df_selected.to_dict(orient='records')
        
        return listDates
    except FileNotFoundError:
        print("El archivo Excel no se encontró.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo Excel: {e}")
        return []

def current(init: str, end: str) -> str:
    """
        Current crea un string con la cadena de texto de la fecha a usar en el formato Pdf.
        Args:
            init (str): Fecha inicial de los extractos.
            end (str): Fecha final de los extractos.
        Returns:
            str: La fecha formateada para los Pdfs.
    """
    monthsYear = {
    "01": 'Enero',
    "02": 'Febrero',
    "03": 'Marzo',
    "04": 'Abril',
    "05": 'Mayo',
    "06": 'Junio',
    "07": 'Julio',
    "08": 'Agosto',
    "09": 'Septiembre',
    "10": 'Octubre',
    "11": 'Noviembre',
    "12": 'Diciembre'
}
    dates = init.split("-")
    start = dates[2]
    last = end.split("-")[2]
    month = monthsYear[dates[1]]
    return f"{start} al {last} de {month} del {dates[0]}"

def countMoves(listMoves: list, valueInit: int) -> Tuple[List[dict], int, int]:
    """Calcula y crea una lista de movimientos junto con su saldo actual en cada movimiento,
    a su vez calcula y suma cada uno de los debitos y creditos de todos los movimientos.

    Args:
        listMoves (list): Lista de los movimientos.
        valueInit (int): Valor inicial de la cuenta.

    Returns:
        tupla(list, int, int): 
            list: Lista de movimientos jutno con el calculo de los debidos y creditos en el saldo inicial.
            int: La suma de los debitos totales.
            int: La suma de los creditos totales. 
    """
    newList = []
    currentValue = valueInit
    dbTotal = 0
    cdTotal = 0
    for date in listMoves:
        # Crea un nuevo objeto con los datos necesarios para cada movimiento
        datesMoves = {}
        datesMoves["fecha"] = str(date['F_MOVIMI']).split(' ')[0]
        datesMoves["descripcion"] = str(date['N_MOVIMI']).lower().capitalize()
        datesMoves["numMov"] = str(date['K_NUMDOC'])
        datesMoves["lugar"] = "Bogotá"
        
        datesMoves["debito"] = str(date['V_DBPESO'])
        dbTotal += int(date['V_DBPESO'])
        
        datesMoves["credito"] = str(date['V_CRPESO'])
        cdTotal += int(date['V_CRPESO'])
        
        currentValue = currentValue - int(date['V_DBPESO']) + int(date['V_CRPESO'])
        datesMoves["total"] = str(currentValue)
        newList.append(datesMoves)
    return newList, dbTotal, cdTotal

def main():
    """Funcion main recupera todos los datos, usuarios, movimientos y cuentas.
        Recorre cada uno de los usuarios y crea el archivo pdf y excel de los movimientos.
    """
    # Recupera los datos de los usuarios o cuentas
    usersData = usersBase()
    
    # Recupera todos los movimientos de las cuentas
    movimentsData = movsBase()

    # Recupera las cuentas interbancarias
    listCuentas = cuentaInter()
    
    usersList = []
    listUsersNotCuentaInterbancaria = []
    listUsersNotFoundCuentaInterbancaria = []
    # Recorre uno a uno los users o cuentas
    for user in usersData:
        userStructure = {}
        userStructure["username"] = user["NNASOCIA"]
        userStructure["id"] = str(user["AANUMNIT"])
        userStructure["cuenta"] = str(user["N_CUENTA"])
        filterCuentaInt = ""
        try:
            filterCuentaInt = [str(cuentInt['Cuenta Interbancaria']) for cuentInt in listCuentas if int(cuentInt["documento"]) == int(user["AANUMNIT"])][0]
        except IndexError:
            listUsersNotCuentaInterbancaria.append(user['AANUMNIT'])
            listUsersNotFoundCuentaInterbancaria.append(user['N_CUENTA'])
        userStructure["cuentaInt"] = filterCuentaInt if filterCuentaInt else "00000000000"
        
        userStructure["fecha"] = current(str(user["F_INI"]).split(" ")[0], str(user["F_FIN"]).split(" ")[0])
        userStructure["estado"] = "CANCELADA" if user["I_ESTADO"] == "C" else "ACTIVO"
        userStructure["saldo_anterior"] = str(user["SALDOINI"])
        userStructure["saldo_actual"] = str(user["SALDOFIN"])
        listMoves = [movs for movs in movimentsData if user["K_CUENTA"] == movs["K_CUENTA"]]
        
        movimientos, dbTotal, cdTotal = countMoves(listMoves, user["SALDOINI"])
        
        userStructure["movimientos"] = movimientos
        userStructure["debitos"] = dbTotal
        userStructure["creditos"] = cdTotal
        
        if userStructure["estado"] == "CANCELADA" and userStructure["movimientos"] == [] and int(userStructure["saldo_anterior"]) == 0 and int(userStructure["saldo_actual"] == 0):
            continue
        # if userStructure["id"] == "900161467" or userStructure['id'] == "900328654":
        usersList.append(userStructure)

    # Crear un archivo excel con todas las cuentas de ahorro que no tienen cuenta interbancaria
    
    df = pd.DataFrame({
        'NIT': listUsersNotCuentaInterbancaria,
        'Cuenta': listUsersNotFoundCuentaInterbancaria,
    })
    
    df = df[['NIT', 'Cuenta']]
    
    nameFile = f"cuentasNotFound.xlsx"
    writer = ExcelWriter(nameFile)
    
    df.to_excel(writer, 'Hoja 1', index=False)
    
    writer.close()
    


    for user in usersList:
        # Crear el documento
        
        # Estructura el nombre requerido para crear cada PDF
        dateFile = user['fecha'].split(" ")
        nameFile = f"{dateFile[4][:3].upper()}-{dateFile[6]}_ID_"
        name = f"{nameFile}{user['id']}_EXTRACTO_CTA_AHORRO.PDF"
        nameExcel = f"{nameFile}{user['id']}_EXTRACTO_CTA_AHORRO.xlsx"
        # Crea el pdf
        if os.path.exists(f"pdfs/{name}"):
            for index in range(10):
                name = f"{nameFile}{user['id']}_EXTRACTO_CTA_AHORRO({index}).PDF"
                if os.path.exists(f"pdfs/{name}"):
                    continue
                else:
                    break
        doc = BaseDocTemplate(f"pdfs/{name}", pagesize=letter)

        # Definir el estilo de los elementos del documento
        styles = getSampleStyleSheet()

        def on_page(canvas, doc):
            """
                on_page genera la estructura estandar para cada una de las hojas creadas en los pdfs.
            """
            
            # Imagen de logo de coovitel que se agrega al documento
            canvas.drawImage("images/coovitel.png", 40, 720, width=190, height=45)
            
            # Datos de coovitel que se reflejan en el pdf
            canvas.setFillColorRGB(0.176, 0.200, 0.416)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(260, 750, f"COOPERATIVA EMPRESARIAL DE AHORRO Y CRÉDITO")
            canvas.drawString(310, 737, f"EXTRACTO CUENTA DE AHORROS")
            canvas.drawString(360, 724, f"Nit: 860015017-0")
            
            # Datos y numero de cuenta del titular del producto
            canvas.setFillColorRGB(0, 0, 0)
            canvas.setFont("Helvetica-Bold", 8)
            canvas.drawString(45, 700, f"{user['id']}")
            canvas.drawString(45, 692, f"{user['username']}")
            
            #Rectangulo 
            canvas.roundRect(330, 682, width=225, height=37, radius=3)
            
            # Imagen publicitaria dentro del pdf
            canvas.drawImage("images/imagepdf.jpeg", 45, 490, width=515, height=187)
            
            # Datos de numero de producto cuenta y estado del titular del extracto
            canvas.setFillColorRGB(0.430, 0.470, 0.470)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(45, 470, f"Cuenta Coopcentral")
            canvas.drawString(48, 457, f"00{user['cuentaInt']}")
            canvas.drawString(190, 470, f"Cuenta de Ahorros Coovitel")
            canvas.drawString(190, 457, f"{user['cuenta']}")
            canvas.drawString(45, 440, f"Estado: {user['estado']}")
            
            # Rectangulo para la fecha del documento
            canvas.roundRect(390, 445, width=165, height=32, radius=3, stroke=1)
            
            # Fecha o periodo del extracto
            canvas.setFillColorRGB(0, 0, 0)
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(430, 465, f"Periodo del informe")
            canvas.setFont("Helvetica", 9)
            canvas.drawString(410, 452, f"{user['fecha']}")
            
            # Tabla principal con los datos finales dentro del documento
            data = [
                ['Saldo Anterior', 'Débitos', 'Créditos', 'Saldo Actual'],
                [
                    format(int(float(user['saldo_anterior'])), ','), 
                    format(int(float(user['debitos'])), ','), 
                    format(int(float(user['creditos'])), ','), 
                    format(int(float(user['saldo_actual'])), ',')
                ]
            ]

            # Definicion de tamaño de cada una de las columnas dentro del documento
            table = Table(data, colWidths=130)
            # Estilos de la tabla general 
            table.setStyle(TableStyle([
                ('ROUNDEDCORNERS', [4, 4, 4, 4]),            
                ('BOX', (0, 0), (-1, -1), 0.25, (0,0,0)), # Agrega un borde alrededor de toda la tabla
                ('INNERGRID', (0, 0), (-1, -1), 0.25, (0,0,0)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            # Definicion de posicion en la cual se agrega la tabla dentro del documento
            table.wrapOn(canvas, 390, 220)
            table.drawOn(canvas, 45, 390)
            
            # Logo de la super solidaria
            canvas.drawImage("images/super.png", 0, 490, width=45, height=140)
            
            # Recuadro de lineas de atencion
            canvas.roundRect(40, 35, width=135, height=60, radius=5, stroke=1)
            canvas.drawImage("images/phone.png", 42, 39, width=37, height=55)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(80, 75, "Linea de atención")
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(82, 62, "018000967474")
            canvas.setFont("Helvetica-Bold", 13)
            canvas.drawString(80, 47, "(601) 5666601")
            
            # Recuado medio inferior adjunto con la informacion de contanto, direccion principal y de la oficina tunja
            canvas.roundRect(185, 35, width=240, height=60, radius=5, stroke=1)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(260, 75, "www.coovitel.coop")
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(212, 60, "Dirrección general: Calle 67# 9 - 34 Bogotá")
            canvas.drawString(197, 45, "Oficina Tunja: Carrera 10 # 17 - 57 Centro Histórico")
            
            # Logo de fogacoop
            canvas.roundRect(435, 35, width=135, height=60, radius=5, stroke=1)
            canvas.drawImage("images/fogacoop.png", 443, 40, width=120, height=50)
            
            # Numero de pagina, junto con su posicion dentro del pdf
            canvas.drawString(290, 15, f"Página {doc.page}")


        # Crear un PageTemplate con un Frame
        frame = Frame(doc.leftMargin + 48, doc.bottomMargin + 15, doc.width - 100, doc.height - 350, id='mainFrame')


        template = PageTemplate(id='mainTemplate', frames=frame, onPage=on_page)

        # Añadir el PageTemplate al documento
        doc.addPageTemplates([template])

        # Definicion de las columnas prensentes en la segunda tabla, la cual contendra
        # los movimientos de los extractos del titular en PDF
        data = [
            ['Fecha', 'Transacción', 'Documento', 'Débito', 'Crédito', 'Saldos'],
        ]
        
        # Loop que agrega los movimientos dentro de la lista de movimientos y a las listas de las columnas excel
        dates, description, credito, debito, number, año, saldo = [], [], [], [], [], [], []
        
        for mov in user['movimientos']:
            # Datos para el documento excel
            date = mov['fecha'].split("-")
            date.reverse()
            setDate = "/".join(date)
            
            dates.append(setDate)
            number.append(int(mov['numMov']))
            description.append(mov['descripcion'])
            año.append(int(mov['fecha'].split("-")[0]))
            debito.append(format(int(mov['debito']), ','))
            credito.append(format(int(mov['credito']), ','))
            try:
                # Intenta convertir la cadena a un entero
                saldo.append(format(int(mov['total']), ','))
            except ValueError:
                # Si falla, convierte la cadena a un float y luego a un entero
                saldo.append(format(int(float(mov['total'])), ','))
            
            # Datos para el documento pdf
            try:
                # Intenta convertir la cadena a un entero
                total = format(int(mov['total']), ',')
            except ValueError:
                # Si falla, convierte la cadena a un float y luego a un entero
                total = format(int(float(mov['total'])), ',')
                
            movs = [
                str(mov['fecha']),
                str(mov['descripcion'])[0:34] + "...",
                str(mov['numMov']),
                format(int(mov['debito']), ','),
                format(int(mov['credito']), ','),
                total
            ]
            data.append(movs)
        
        # Definicion de los estilos a la tabla de movimientos
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleN.wordWrap = 'CJK'
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7

        # Crear un estilo para las primeras tres filas con un tamaño de fuente diferente
        styleN_large = styleN.clone('styleN_large')
        styleN_large.fontSize = 9.5 # Tamaño de fuente más grande para las primeras tres filas

        # Generar las filas de la tabla con el estilo modificado para las primeras tres filas
        data2 = [[Paragraph(cell, styleN_large if i == 0 else styleN) for cell in row] for i, row in enumerate(data)]
                
        colWidth = [60, 180, 64, 70, 70, 70] # 514
        
        table = Table(data2, colWidths=colWidth)
        tableStyle = [
            ('TEXTCOLOR', (0, 0), (-1, 0), (0,0,0)),
            ('GRID', (0,0), (-1,-1), 0.1, (0,0,0)),
            ('VALING', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
            ('PADDING', (0, 0), (-1, -1), 0),
        ]
        
        table.setStyle(tableStyle)

        # Añadir el contenido al documento
        story = [table]

        # Construir el documento
        doc.build(story)    
        
        # Crea el documento Excel
        df = pd.DataFrame({
            'Fecha': dates,
            'Numero': number,
            'Año': año,
            'Descripción': description,
            'Debito': debito,
            'Credito': credito,
            'Saldo': saldo
        })
        
        df = df[['Fecha', 'Numero', 'Año', 'Descripción', 'Debito', 'Credito', 'Saldo']]
        
        nameFile = f"excels/{nameExcel}"
        if os.path.exists(f"excels/{nameExcel}"):
            for index in range(10):
                nameExcel = f"{nameFile}{user['id']}_EXTRACTO_CTA_AHORRO({index}).xlsx"
                if os.path.exists(f"excels/{nameExcel}"):
                    continue
                else:
                    break
        writer = ExcelWriter(nameFile)
        
        df.to_excel(writer, 'Hoja 1', index=False)
        
        writer.close()
        
        pdf_reader = PdfReader(f"pdfs/{name}")
        pdf_writer = PdfWriter()
        
        # Encriptar PDF
        user_pwd = user['id']
        pdf_writer.encrypt(user_pwd, use_128bit=True)
        
        # copiar las paginas del pdf original al nuevo PDF encriptado
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
        #Guardar el PDF encriptado
        with open(f"pdfs/{name}", "wb") as out_pdf:
            pdf_writer.write(out_pdf)

if __name__ == '__main__':
    main()