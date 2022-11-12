from modulos import *


class Relatorios:

    def printEncomenda(self):
        webbrowser.open("encomenda.pdf")

    def geraRelatEncomenda(self):
        self.conecta_bd()

        self.variaveis()

        self.c = canvas.Canvas("encomenda.pdf", pagesize=A4)
        codigo = self.codigo_entry.get()
        tabela = pd.read_sql(f"""SELECT codigo, destinatario, data_entrada, tipo, 
                                        funcionario, data_retirada,  retirada_por
                                FROM quarentena_bd
                                WHERE codigo 
                                LIKE '%{codigo}%'""", self.conn)

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 670, 'Código: ')
        self.c.drawString(50, 630, 'Destinatário(a): ')
        self.c.drawString(50, 600, 'Data de Entrada: ')
        self.c.drawString(50, 570, 'Tipo: ')
        self.c.drawString(50, 530, 'Funcionário(a): ')
        self.c.drawString(50, 500, 'Data de Retirada: ')
        self.c.drawString(50, 470, 'Retirado por: ')

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(130, 670, str(tabela['codigo'][0]))
        self.c.drawString(190, 630, str(tabela['destinatario'][0]))
        self.c.drawString(200, 600, str(tabela['data_entrada'][0]))
        self.c.drawString(100, 570, str(tabela['tipo'][0]))
        self.c.drawString(190, 530, str(tabela['funcionario'][0]))
        self.c.drawString(205, 500, str(tabela['data_retirada'][0]))
        self.c.drawString(170, 470, str(tabela['retirada_por'][0]))

        self.c.showPage()
        self.c.save()
        self.printEncomenda()
        self.desconecta_bd()
