from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from dataSource import data as DataUsers


def main():
    dataUsers = DataUsers.data
    
    for user in dataUsers:
        # Crear el documento
        doc = BaseDocTemplate(f"pdfs/{user['username']}.pdf", pagesize=letter)

        # Definir el estilo de los elementos del documento
        styles = getSampleStyleSheet()

        def on_page(canvas, doc):
            canvas.drawImage("images/coovitel.png", 40, 720, width=190, height=45)
            
            canvas.setFillColorRGB(0.176, 0.200, 0.416)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(260, 750, f"COOPERATIVA EMPRESARIAL DE AHORRO Y CRÉDITO")
            canvas.drawString(310, 737, f"EXTRACTO CUENTA DE AHORROS")
            canvas.drawString(360, 724, f"Nit: 860015017-0")
            
            canvas.setFillColorRGB(0, 0, 0)
            canvas.setFont("Helvetica-Bold", 8)
            canvas.drawString(45, 700, f"891800186")
            canvas.drawString(45, 692, f"MUNICIPIO {user['city']}")
            
            canvas.roundRect(330, 682, width=225, height=37, radius=3)
            
            canvas.drawImage("images/imagepdf.png", 45, 490, width=515, height=187)
            
            canvas.setFillColorRGB(0.430, 0.470, 0.470)
            canvas.setFont("Helvetica-Bold", 11)
            canvas.drawString(45, 470, f"Cuenta Coopcentral")
            canvas.drawString(48, 457, f"{user['cuenta']}")
            
            canvas.drawString(190, 470, f"Cuenta de Ahorros Coovitel")
            canvas.drawString(190, 457, f"{user['cuenta']}")
            
            canvas.drawString(45, 440, f"Estado: {user['estado']}")
            
            canvas.roundRect(390, 445, width=165, height=32, radius=3, stroke=1)
            
            canvas.setFillColorRGB(0, 0, 0)
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(430, 465, f"Periodo del informe")
            canvas.setFont("Helvetica", 9)
            canvas.drawString(410, 452, f"01 de Febrero al 29 Febrero 2024")
            
            data = [
                ['Saldo Anterior', 'Débitos', 'Créditos', 'Saldo Actual'],
                [user['saldo_anterior'], user['debitos'], user['creditos'], user['saldo_actual']]
            ]  
            table = Table(data, colWidths=130)
            table.setStyle(TableStyle([
                ('ROUNDEDCORNERS', [4, 4, 4, 4]),            
                ('BOX', (0, 0), (-1, -1), 0.25, (0,0,0)), # Agrega un borde alrededor de toda la tabla
                ('INNERGRID', (0, 0), (-1, -1), 0.25, (0,0,0)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            table.wrapOn(canvas, 390, 220)
            table.drawOn(canvas, 45, 390)
                                
            canvas.drawImage("images/super.png", 0, 490, width=45, height=140)
            
            canvas.roundRect(40, 35, width=135, height=60, radius=5, stroke=1)
            canvas.drawImage("images/phone.png", 42, 39, width=37, height=55)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(80, 75, "Linea de atención")
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(82, 62, "018000967474")
            canvas.setFont("Helvetica-Bold", 13)
            canvas.drawString(80, 47, "(601) 5666601")
            
            canvas.roundRect(185, 35, width=240, height=60, radius=5, stroke=1)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(260, 75, "www.coovitel.coop")
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawString(212, 60, "Dirrección general: Calle 67# 9 - 34 Bogotá")
            canvas.drawString(197, 45, "Oficina Tunja: Carrera 10 # 17 - 57 Centro Histórico")
            
            
            canvas.roundRect(435, 35, width=135, height=60, radius=5, stroke=1)
            canvas.drawImage("images/fogacoop.png", 443, 40, width=120, height=50)
            
            canvas.drawString(290, 15, f"Página {doc.page}")

        # Crear un PageTemplate con un Frame
        frame = Frame(doc.leftMargin + 48, doc.bottomMargin + 15, doc.width - 100, doc.height - 350, id='mainFrame')


        template = PageTemplate(id='mainTemplate', frames=frame, onPage=on_page)

        # Añadir el PageTemplate al documento
        doc.addPageTemplates([template])

        # Crear el contenido del documento (por ejemplo, una tabla)
        data = [
            ['Fecha', 'Transacción', 'Documento', 'Sucursal', 'Débito', 'Crédito', 'Saldos'],
        ]
        
        for mov in user['movimientos']:
            movs = [
                str(mov['fecha']),
                str(mov['lugar']),
                str(mov['documento']),
                str(mov['sucursal']),
                str(mov['debito']),
                str(mov['credito']),
                str(mov['saldos'])
            ]
            data.append(movs)
        
        
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

if __name__ == '__main__':
    main()
