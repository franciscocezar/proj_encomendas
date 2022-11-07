from modulos import *
from funcionalidades import Funcs


class Relatorios:

    def printEncomenda(self):
        webbrowser.open("encomenda.pdf")

    def geraRelatEncomenda(self):
        self.variaveis()

        self.c = canvas.Canvas("encomenda.pdf")

        self.idRel = self.id_entry.get()
        self.codigoRel = self.codigo_entry.get()
        self.destinatarioRel = self.destinatario_entry.get()
        self.dataentradaRel = self.dataentrada
        self.tipoRel = self.tipo_entry.get()
        self.funcionarioRel = self.funcionario_entry.get()
        # self.data_retiradaRel = self.data_retirada
        # self.retiradoporRel = self.retirada_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'ID: ')
        self.c.drawString(50, 670, 'Código: ')
        self.c.drawString(50, 630, 'Destinatário(a): ')
        self.c.drawString(50, 600, 'Data de Entrada: ')
        self.c.drawString(50, 570, 'Tipo: ')
        self.c.drawString(50, 530, 'Funcionário(a): ')
        self.c.drawString(50, 500, 'Data de Retirada: ')
        self.c.drawString(50, 470, 'Retirado por: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(100, 700, self.idRel)
        self.c.drawString(130, 670, self.codigoRel)
        self.c.drawString(200, 630, self.destinatarioRel)
        self.c.drawString(200, 600, self.dataentradaRel)
        self.c.drawString(110, 570, self.tipoRel)
        self.c.drawString(200, 530, self.funcionarioRel)
        # self.c.drawString(230, 500, self.data_retiradaRel)
        # self.c.drawString(200, 470, self.retiradoporRel)

        self.c.showPage()
        self.c.save()
        self.printEncomenda()
