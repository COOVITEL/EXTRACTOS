from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
from reportlab.platypus import Table, TableStyle

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
        c = canvas.Canvas(f"{user['name']}.pdf")

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
            ('ROUNDEDCORNERS', (0, 0), (-1, -1), 100),
            ('BOX', (0, 0), (-1, -1), 0.25, (0,0,0)), # Agrega un borde alrededor de toda la tabla
            ('INNERGRID', (0, 0), (-1, -1), 0.25, (0,0,0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        
        table.wrapOn(c, 500, 200)
        table.drawOn(c, 45, 400)
        
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
