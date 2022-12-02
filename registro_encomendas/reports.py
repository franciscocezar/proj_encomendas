from modulos import *


class Relatorios:
    def printEncomenda(self):
        webbrowser.open('../encomenda.pdf')

    def geraRelatEncomenda(self):
        self.conecta_bd()

        self.variaveis()

        self.c = canvas.Canvas(
            '/Users/franciscojunior/Downloads/encomendas_proj_exe/registro_encomendas/encomenda.pdf',
            pagesize=A4,
        )
        codigo = self.codigo_entry.get()

        self.cursor.execute(f"""SELECT * FROM Quarentena WHERE codigo LIKE '%{codigo}%' """)
        colunas = self.cursor.fetchall()
        for i in colunas:
            col0 = i[0]
            col1 = i[1]
            col2 = i[2]
            col3 = i[3]
            col4 = i[4]
            col5 = i[5]
            col6 = i[6]

        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        self.c.setFont('Helvetica-Bold', 18)
        self.c.drawString(50, 670, 'Código: ')
        self.c.drawString(50, 630, 'Destinatário(a): ')
        self.c.drawString(50, 600, 'Data de Entrada: ')
        self.c.drawString(50, 570, 'Tipo: ')
        self.c.drawString(50, 530, 'Funcionário(a): ')
        self.c.drawString(50, 500, 'Data de Retirada: ')
        self.c.drawString(50, 470, 'Retirado por: ')

        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        self.c.setFont('Helvetica', 18)
        self.c.drawString(130, 670, col0)
        self.c.drawString(190, 630, col1)
        self.c.drawString(200, 600, col2)
        self.c.drawString(100, 570, col3)
        self.c.drawString(190, 530, col4)
        self.c.drawString(205, 500, col5)
        self.c.drawString(170, 470, col6)

        self.c.showPage()
        self.c.save()
        self.printEncomenda()
        self.desconecta_bd()
