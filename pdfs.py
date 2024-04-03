#!/usr/bin/python3
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
from reportlab.platypus import Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter


def main():

    users = [
        {
            'name': 'Manu',
            'cedula': '123456',
        },
        {
            'name': 'Esteban',
            'cedula': '987654',
        }
    ]

    for user in users:
        c = canvas.Canvas(f"pdfs/{user['name']}.pdf", pagesize=letter)

        c.drawImage("images/coovitel.png", 40, 740, width=190, height=45)
        
        c.setFillColorRGB(0.176, 0.200, 0.416)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(250, 770, f"COOPERATIVA EMPRESARIAL DE AHORRO Y CRÉDITO")
        c.drawString(300, 757, f"EXTRACTO CUENTA DE AHORROS")
        c.drawString(350, 744, f"Nit: 860015017-0")
        
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(45, 720, f"891800186")
        c.drawString(45, 712, f"MUNICIPIO TUNJA")
        
        c.roundRect(320, 702, width=225, height=37, radius=3)
        
        c.drawImage("images/imagepdf.png", 45, 515, width=500, height=180)
        
        c.setFillColorRGB(0.430, 0.470, 0.470)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(45, 490, f"Cuenta Coopcentral")
        c.drawString(48, 480, f"0037000003823")
        
        c.drawString(190, 490, f"Cuenta de Ahorros Coovitel")
        c.drawString(190, 480, f"110113570")
        
        c.drawString(45, 460, f"Estado: Activo")
        
        c.roundRect(380, 475, width=165, height=32, radius=3, stroke=1)
        
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(420, 495, f"Periodo del informe")
        c.setFont("Helvetica", 9)
        c.drawString(400, 482, f"01 de Febrero al 29 Febrero 2024")
        
        
        data = [
            ['Saldo Anterior', 'Débitos', 'Créditos', 'Saldo Actual'],
            ['11.174.176.561', '5.000.000.000', '107.983.377', '6.282.159.938']
        ]  
        table = Table(data, colWidths=125)
        table.setStyle(TableStyle([
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),            
            ('BOX', (0, 0), (-1, -1), 0.25, (0,0,0)), # Agrega un borde alrededor de toda la tabla
            ('INNERGRID', (0, 0), (-1, -1), 0.25, (0,0,0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        table.wrapOn(c, 500, 200)
        table.drawOn(c, 45, 400)
        
        
        
        movements = [
            ['Fecha', 'Transacción', 'Documento', 'Sucursal', 'Débito', 'Crédito', 'Saldos']
        ]
        moves = [
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
            ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
            ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
            ['20-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
                        ['02-FEB-24', 'ABONO RECAUDO IMPUESTO MUNICIPALES 02FEB2024', '11000607', '11', '0', '428.000', '11.174.604.561'],
            ['12-FEB-24', 'SOLICITUD TRANSLADO FONDOS PAD_142-10076 DE FEBRERO 12 PARA LA CUENTA CORRIENTE BANCO OCCIDENTE', '11000078', '11', '5.000.000.000', '0', '6.174.604.561'],
            ['14-FEB-24', 'ABONO RECAUDO IMPUESTO SMUNICIPALES 14FEB2024', '1120000002', '11', '0', '5.794.000', '6.180.398.561'],
            ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
            ['16-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
            ['20-FEB-24', 'ABONO RECAUDO IMPUESTO', '11000607', '11', '0', '428.000', '11.174.604.561'],
        ]
        movements += [mov for mov in moves]
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleN.wordWrap = 'CJK'
        styleN.fontSize = 7
        styleN.alignment = TA_CENTER
        
        data2 = [[Paragraph(cell, styleN) for cell in row] for row in movements]
            
        colWidth = [50, 130, 60, 45, 75, 75, 75]
                
        t = Table(data2, colWidths=colWidth)
        
        tableStyle = [
            ('ROUNDEDCORNERS', [4, 4, 4, 4]),
            ('BOX', (0, 0), (-1, -1), 0.25, (0,0,0)), # Agrega un borde alrededor de toda la tabla
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALING', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1.2, (0, 0, 0)),
            ('FONTSIZE', (0, 0), (-1, -1), 15)
        ]
        
        t.setStyle(TableStyle(tableStyle))
        rows_per_page = 10
        for i in range(0, len(data2), rows_per_page):
            # Dibuja solo las filas que caben en la página actual
            t.wrapOn(c, 800, rows_per_page * 100)
            t.drawOn(c, 40, -500)

            # Si hay más filas, comienza una nueva página
            if i + rows_per_page < len(data2):
                c.showPage()
        
        c.save()
    

        """
        pdf_reader = PdfReader(f"{user['name']}.pdf")
        pdf_writer = PdfWriter()

        # Encriptar el PDF
        user_pwd = user['cedula']
        pdf_writer.encrypt(user_pwd, use_128bit=True)

        # Copiar las páginas del PDF original al nuevo PDF encriptado
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        # Guardar el PDF encriptado
        with open(f"{user['name']}.pdf", "wb") as out_pdf:
            pdf_writer.write(out_pdf)
        """

if __name__ == '__main__':
    main()
