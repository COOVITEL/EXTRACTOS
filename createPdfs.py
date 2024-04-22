from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from dataSource import data as DataUsers
from dataSource.usersBase import usersBase
from dataSource.movsUsersBase import movsBase
from time import time
import pandas as pd
from pandas import ExcelWriter
from datetime import datetime
from dataSource.generate_mov import generate_mov
import random
import currentDate



def current(init, end):
    """"""
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
    return f"{start} de {month} al {last} {dates[0]}"


def main():
    star_time = time()
    
    usersData = usersBase()
    movimentsData = movsBase()
    
    usersList = []
    for user in usersData:
        if user["SALDOINI"] != 0 or user["SALDOFIN"]:
            userStructure = {}
            userStructure["username"] = user["NNASOCIA"]
            userStructure["id"] = str(user["AANUMNIT"])
            userStructure["cuenta"] = str(user["N_CUENTA"])
            userStructure["fecha"] = current(str(user["F_INI"]).split(" ")[0], str(user["F_FIN"]).split(" ")[0])
            userStructure["estado"] = "CANCELADA" if user["I_ESTADO"] == "C" else "ACTIVO"
            userStructure["saldo_anterior"] = str(user["SALDOINI"])
            userStructure["saldo_actual"] = str(user["SALDOFIN"])
            userStructure["debitos"] = str(0)
            userStructure["creditos"] = str(0)
            userStructure["movimientos"] = [movs for movs in movimentsData if user["K_CUENTA"] == movs["K_CUENTA"]]
            usersList.append(userStructure)
        
    for user in usersList:
        # Crear el documento
        doc = BaseDocTemplate(f"pdfs/{user['username']}.pdf", pagesize=letter)

        # Definir el estilo de los elementos del documento
        styles = getSampleStyleSheet()

        def on_page(canvas, doc):
            # Esta funcion crea el etilo general para todas las hojas que se creen dentro del pdf
            
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
            canvas.drawImage("images/imagepdf.png", 45, 490, width=515, height=187)
            
            # Datos de numero d eproducto cuenta y estado del titular del extracto
            canvas.setFillColorRGB(0.430, 0.470, 0.470)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(45, 470, f"Cuenta Coopcentral")
            canvas.drawString(48, 457, f"{user['cuenta']}")
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
                [user['saldo_anterior'], user['debitos'], user['creditos'], user['saldo_actual']]
            ]
            # Definicion de tamaño de cada una de las columnas dentro del documento
            table = Table(data, colWidths=130)
            # Estilos de lla tabla general 
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
        # los movimientos de los extractos del titular
        data = [
            ['Fecha', 'Transacción', 'Documento', 'Sucursal', 'Débito', 'Crédito', 'Saldos'],
        ]
        
        # Loop que agrega los movimientos dentro de la lista de movimientos y a las listas de las columnas excel
        dates, description, credito, debito, number, año, saldo = [], [], [], [], [], [], []
        
        for mov in user['movimientos']:
            # Datos para el documento excel
            #currentDate = datetime.strptime(str(mov['F_MOVIMI']).split(" ")[1], "%d-%b-%y")
            currentDateMov = str(mov['F_MOVIMI']).split(' ')[0]
            dates.append(currentDateMov)
            number.append(mov['K_NUMDOC'])
            year = currentDateMov.split("-")[0]
            año.append(year)
            description.append(mov['N_MOVIMI'])
            debito.append(mov['V_DBPESO'])
            credito.append(mov['V_CRPESO'])
            saldo.append(mov['V_CANJ'])
            # Datos para el documento pdf
            movs = [
                str(mov['F_MOVIMI']).split(' ')[0],
                str(mov['N_MOVIMI']).lower().capitalize()[0:40],
                str(mov['K_NUMDOC']),
                "Bogotá",
                str(mov['V_DBPESO']),
                str(mov['V_CRPESO']),
                str(mov['V_CANJ'])
            ]
            data.append(movs)
        
        # Definicion de los estilos a la tabla de movimientos
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleN.wordWrap = 'CJK'
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7.5

        # Crear un estilo para las primeras tres filas con un tamaño de fuente diferente
        styleN_large = styleN.clone('styleN_large')
        styleN_large.fontSize = 9 # Tamaño de fuente más grande para las primeras tres filas

        # Generar las filas de la tabla con el estilo modificado para las primeras tres filas
        data2 = [[Paragraph(cell, styleN_large if i == 0 else styleN) for cell in row] for i, row in enumerate(data)]
                
        colWidth = [60, 125, 60, 51, 73, 73, 73]
        
        table = Table(data2, colWidths=colWidth)
        tableStyle = [
            ('TEXTCOLOR', (0, 0), (-1, 0), (0,0,0)),
            ('GRID', (0,0), (-1,-1), 0.1, (0,0,0)),
            ('VALING', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
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
        
        nameFile = f"excels/{user['username']}.xlsx"
        writer = ExcelWriter(nameFile)
        
        df.to_excel(writer, 'Hoja 1', index=False)
        
        writer.close()
        
        
        
        
    end_time = time()
    
    #print(f"El tiempo inicar es de {star_time}")
    #print(f"El tiempo final es de {end_time}")
    total_time = end_time - star_time
    #print(f"El tiempo final de ejecucion es de {total_time}")
if __name__ == '__main__':
    main()
