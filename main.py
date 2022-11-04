from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

from datetime import datetime

root = Tk()


class Relatorios:

    def printEncomenda(self):
        webbrowser.open("encomenda.pdf")

    def geraRelatEncomenda(self):
        self.c = canvas.Canvas("encomenda.pdf")

        self.idRel = self.id_entry.get()
        self.codigoRel = self.codigo_entry.get()
        self.destinatarioRel = self.destinatario_entry.get()
        self.dataentrada = self.dataentrada_entry.get()
        self.tipoRel = self.tipo_entry.get()
        self.funcionarioRel = self.funcionario_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(150, 790, 'Informações da Encomenda')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'ID: ')
        self.c.drawString(50, 670, 'Código: ')
        self.c.drawString(50, 630, 'Destinatário(a): ')
        self.c.drawString(50, 600, 'Data de Entrada: ')
        self.c.drawString(50, 570, 'Tipo: ')
        self.c.drawString(50, 530, 'Funcionário(a): ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(100, 700, self.idRel)
        self.c.drawString(130, 670, self.codigoRel)
        self.c.drawString(200, 630, self.destinatarioRel)
        self.c.drawString(200, 600, self.dataentrada)
        self.c.drawString(110, 570, self.tipoRel)
        self.c.drawString(200, 530, self.funcionarioRel)

        self.c.showPage()
        self.c.save()
        self.printEncomenda()


class Funcs:

    def limpa_tela(self):
        self.id_entry.delete(0, END)
        self.codigo_entry.delete(0, END)
        self.destinatario_entry.delete(0, END)
        self.tipo_entry.delete(0, END)
        self.funcionario_entry.delete(0, END)
        self.dataentrada_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("bancodados_encomendas.db")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando ao banco de dados")

    def montaTabelas(self):
        self.conecta_bd()

        # Criar Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Encomendas(
                id INTEGER PRIMARY KEY,
                codigo CHAR(40) NOT NULL,
                destinatario CHAR(40) NOT NULL,
                data_entrada DATE,
                tipo CHAR(20),
                funcionario CHAR(40)
            );
        """)
        self.conn.commit()
        print("Bando de dados criado")
        self.desconecta_bd()

    def data_hora(self):
        dh = datetime.now()
        return dh.strftime("%d/%m/%Y %H:%M")

    def variaveis(self):
        self.id = self.id_entry.get()
        self.codigo = self.codigo_entry.get().upper()
        self.destinatario = self.destinatario_entry.get().title()
        self.tipo = self.tipo_entry.get().title()
        self.funcionario = self.funcionario_entry.get().title()
        self.dataentrada = self.data_hora()

    def OnDoubleClick(self, event):
        self.limpa_tela()

        for n in self.listaEnc.selection():
            col1, col2, col3, col4, col5, col6 = self.listaEnc.item(n, 'values')
            self.id_entry.insert(END, col1)
            self.codigo_entry.insert(END, col2)
            self.destinatario_entry.insert(END, col3)
            self.dataentrada_entry.insert(END, col4)
            self.tipo_entry.insert(END, col5)
            self.funcionario_entry.insert(END, col6)

    def add_encomenda(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO Encomendas (codigo, destinatario, data_entrada, tipo, funcionario) 
            VALUES (?, ?, ?, ?, ?)""", (self.codigo, self.destinatario, self.dataentrada, self.tipo, self.funcionario))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def altera_dados(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" 
            UPDATE Encomendas 
            SET codigo = ?, destinatario = ?, data_entrada = ?, tipo = ?, funcionario = ?
            WHERE id = ? """, (self.codigo, self.destinatario, self.dataentrada, self.tipo, self.funcionario, self.id))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def deleta_encomenda(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM Encomendas WHERE id = ? """, (self.id,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def select_lista(self):
        self.listaEnc.delete(*self.listaEnc.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT id, codigo, destinatario, data_entrada, tipo, funcionario FROM Encomendas
            ORDER BY destinatario ASC; """)
        for i in lista:
            self.listaEnc.insert("", END, values=i)
        self.desconecta_bd()

    def busca_encomenda(self):
        self.conecta_bd()
        self.listaEnc.delete(*self.listaEnc.get_children())
        self.destinatario_entry.insert(END, '%')
        nome = self.destinatario_entry.get()
        self.cursor.execute("""
            SELECT id, codigo, destinatario, data_entrada, tipo, funcionario 
            FROM Encomendas
            WHERE destinatario 
            LIKE '%s' 
            ORDER BY destinatario ASC""" % nome)

        buscanomeEnc = self.cursor.fetchall()

        for i in buscanomeEnc:
            self.listaEnc.insert("", END, values=i)

        self.limpa_tela()
        self.desconecta_bd()


class Application(Funcs, Relatorios):

    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Registro de Encomendas")
        self.root.configure(bg='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=750, height=600)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # Botão Limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar", bd=2, bg='#107db2', fg='black',
                                font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg='#107db2', fg='black',
                                font=('verdana', 8, 'bold'), command=self.busca_encomenda)
        self.bt_buscar.place(relx=0.4, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Novo
        self.bt_novo = Button(self.frame_1, text="Novo", bd=2, bg='#107db2', fg='black',
                              font=('verdana', 8, 'bold'), command=self.add_encomenda)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=2, bg='#107db2', fg='black',
                                 font=('verdana', 8, 'bold'), command=self.altera_dados)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg='#107db2', fg='black'
                                , font=('verdana', 8, 'bold'), command=self.deleta_encomenda)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        '''Entrada de Dados'''
        # Entrada ID
        self.id_entry = Entry(self.frame_1)
        self.id_entry.place(relx=0.51, rely=0.1,  relwidth=0.07, relheight=0.15)

        # Label e Entrada Codigo
        self.lb_codigo = Label(self.frame_1, text="Código", bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.20)

        # Label e Entrada Destinatário

        self.lb_destinatario = Label(self.frame_1, text="Destinatário(a)", bg='#dfe3ee', fg='#107db2')
        self.lb_destinatario.place(relx=0.05, rely=0.35)

        self.destinatario_entry = Entry(self.frame_1)
        self.destinatario_entry.place(relx=0.05, rely=0.45, relwidth=0.5)

        # Label e Entrada Tipo de Encomenda
        self.lb_tipo = Label(self.frame_1, text="Tipo", bg='#dfe3ee', fg='#107db2')
        self.lb_tipo.place(relx=0.6, rely=0.35)

        self.tipo_entry = Entry(self.frame_1)
        self.tipo_entry.place(relx=0.6, rely=0.45, relwidth=0.30)

        # Label e Entrada Funcionário
        self.lb_funcionario = Label(self.frame_1, text="Funcionário(a)", bg='#dfe3ee', fg='#107db2')
        self.lb_funcionario.place(relx=0.05, rely=0.6)

        self.funcionario_entry = Entry(self.frame_1)
        self.funcionario_entry.place(relx=0.05, rely=0.7, relwidth=0.5)

        # Label e Entrada Data
        self.lb_dataentrada = Label(self.frame_1, text="Data de Entrada", bg='#dfe3ee', fg='#107db2')
        self.lb_dataentrada.place(relx=0.6, rely=0.6)

        self.dataentrada_entry = Entry(self.frame_1)
        self.dataentrada_entry.place(relx=0.6, rely=0.7, relwidth=0.3)

    def lista_frame2(self):
        self.listaEnc = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaEnc.heading("#0", text="")
        self.listaEnc.heading("#1", text="ID")
        self.listaEnc.heading("#2", text="Código")
        self.listaEnc.heading("#3", text="Destinatário(a)")
        self.listaEnc.heading("#4", text="Data Entrada")
        self.listaEnc.heading("#5", text="Tipo")
        self.listaEnc.heading("#6", text="Funcionário(a)")

        self.listaEnc.column("#0", width=1)
        self.listaEnc.column("#1", width=1)
        self.listaEnc.column("#2", width=90)
        self.listaEnc.column("#3", width=110)
        self.listaEnc.column("#4", width=80)
        self.listaEnc.column("#5", width=70)
        self.listaEnc.column("#6", width=70)

        self.listaEnc.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaEnc.configure(yscrollcommand=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaEnc.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatórios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpar", command=self.limpa_tela)

        filemenu2.add_command(label="Dados Encomenda", command=self.geraRelatEncomenda)


Application()
