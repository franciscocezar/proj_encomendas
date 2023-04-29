from modules import *


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


        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        etiqueta = ['Código:', 'Destinatário(a):', 'Data de Entrada:', 'Tipo:',
                    'Funcionário(a):', 'Data de Retirada:', 'Retirado por:']
        self.c.setFont('Helvetica-Bold', 18)
        count= 670
        for nome in etiqueta:
            self.c.drawString(50, count, nome)
            count -= 40

        self.c.setFont('Helvetica', 18)
        count= 670
        for coluna in colunas:
            for dado in coluna:
                try:
                    self.c.drawString(215, count, dado)
                except AttributeError:
                    self.c.drawString(215, count, '---')
                count -= 40

        x1, y1 = 50, 350
        x2, y2 = 350, 350
        self.c.setLineWidth(1)
        self.c.line(x1, y1, x2, y2)
        self.c.drawString(x1, y1 - 20, "Assinatura")

        self.c.showPage()
        self.c.save()
        self.printEncomenda()
        self.desconecta_bd()
