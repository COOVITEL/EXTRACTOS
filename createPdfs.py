from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER


def main():
    # Crear el documento
    doc = BaseDocTemplate("example.pdf", pagesize=letter)

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
        canvas.drawString(45, 692, f"MUNICIPIO TUNJA")
        
        canvas.roundRect(330, 682, width=225, height=37, radius=3)
        
        canvas.drawImage("images/imagepdf.png", 45, 495, width=510, height=185)
        
        canvas.setFillColorRGB(0.430, 0.470, 0.470)
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(45, 470, f"Cuenta Coopcentral")
        canvas.drawString(48, 457, f"0037000003823")
        
        canvas.drawString(190, 470, f"Cuenta de Ahorros Coovitel")
        canvas.drawString(190, 457, f"110113570")
        
        canvas.drawString(45, 440, f"Estado: Activo")
        
        canvas.roundRect(390, 445, width=165, height=32, radius=3, stroke=1)
        
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(430, 465, f"Periodo del informe")
        canvas.setFont("Helvetica", 9)
        canvas.drawString(410, 452, f"01 de Febrero al 29 Febrero 2024")
        
        data = [
            ['Saldo Anterior', 'Débitos', 'Créditos', 'Saldo Actual'],
            ['11.174.176.561', '5.000.000.000', '107.983.377', '6.282.159.938']
        ]  
        table = Table(data, colWidths=130)
        table.setStyle(TableStyle([
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),            
            ('BOX', (0, 0), (-1, -1), 0.25, (0,0,0)), # Agrega un borde alrededor de toda la tabla
            ('INNERGRID', (0, 0), (-1, -1), 0.25, (0,0,0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        table.wrapOn(canvas, 390, 220)
        table.drawOn(canvas, 45, 390)

    # Crear un PageTemplate con un Frame
    frame = Frame(doc.leftMargin + 50, doc.bottomMargin + 15, doc.width - 100, doc.height - 350, id='mainFrame')


    template = PageTemplate(id='mainTemplate', frames=frame, onPage=on_page)

    # Añadir el PageTemplate al documento
    doc.addPageTemplates([template])

    # Crear el contenido del documento (por ejemplo, una tabla)
    data = [
        ['Fecha', 'Transacción', 'Documento', 'Sucursal', 'Débito', 'Crédito', 'Saldos'],
        ['02-FEB-24', 'ABONO RECAUDO IMPUESTO MUNICIPALES 02FEB2024', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['12-FEB-24', 'SOLICITUD TRANSLADO FONDOS PAD_142-10076 DE FEBRERO 12 PARA LA CUENTA CORRIENTE BANCO OCCIDENTE', '11000078', '11', '5.000.000.000', '0', '6.174.604.561'],
        ['14-FEB-24', 'ABONO RECAUDO IMPUESTO SMUNICIPALES 14FEB2024', '1120000002', '11', '0', '5.794.000', '6.180.398.561'],
        ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['20-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['02-FEB-24', 'ABONO RECAUDO IMPUESTO MUNICIPALES 02FEB2024', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['12-FEB-24', 'SOLICITUD TRANSLADO FONDOS PAD_142-10076 DE FEBRERO 12 PARA LA CUENTA CORRIENTE BANCO OCCIDENTE', '11000078', '11', '5.000.000.000', '0', '6.174.604.561'],
        ['14-FEB-24', 'ABONO RECAUDO IMPUESTO SMUNICIPALES 14FEB2024', '1120000002', '11', '0', '5.794.000', '6.180.398.561'],
        ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['20-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['02-FEB-24', 'ABONO RECAUDO IMPUESTO MUNICIPALES 02FEB2024', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['12-FEB-24', 'SOLICITUD TRANSLADO FONDOS PAD_142-10076 DE FEBRERO 12 PARA LA CUENTA CORRIENTE BANCO OCCIDENTE', '11000078', '11', '5.000.000.000', '0', '6.174.604.561'],
        ['14-FEB-24', 'ABONO RECAUDO IMPUESTO SMUNICIPALES 14FEB2024', '1120000002', '11', '0', '5.794.000', '6.180.398.561'],
        ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['20-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['02-FEB-24', 'ABONO RECAUDO IMPUESTO MUNICIPALES 02FEB2024', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ['12-FEB-24', 'SOLICITUD TRANSLADO FONDOS PAD_142-10076 DE FEBRERO 12 PARA LA CUENTA CORRIENTE BANCO OCCIDENTE', '11000078', '11', '5.000.000.000', '0', '6.174.604.561'],
        ['14-FEB-24', 'ABONO RECAUDO IMPUESTO SMUNICIPALES 14FEB2024', '1120000002', '11', '0', '5.794.000', '6.180.398.561'],
    ]
    
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.wordWrap = 'CJK'
    styleN.fontSize = 6
    styleN.alignment = TA_CENTER
    
    firstRowStyle = getSampleStyleSheet()
    firstRowStyle = styleN
    firstRowStyle.fontSize = 12
    
    data2 = [[Paragraph(cell, firstRowStyle if row == 0 else styleN) for cell in row] for row in data]
            
    colWidth = [50, 130, 60, 45, 75, 75, 75]
    
    table = Table(data2, colWidths=colWidth)
    tableStyle = [
        ('TEXTCOLOR', (0, 0), (-1, 0), (0,0,0)),
        ('GRID', (0,0), (-1,-1), 0.8, (0,0,0)),
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
