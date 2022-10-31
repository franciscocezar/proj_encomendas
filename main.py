from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()


class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nomed_entry.delete(0, END)
        self.tipo_entry.delete(0, END)
        self.nomef_entry.delete(0, END)
        self.dataen_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("bancod_encomendas.db")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando ao banco de dados")

    def montaTabelas(self):
        self.conecta_bd()
        # Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Encomendas(
                id INTEGER PRIMARY KEY,
                codigo CHAR(40),
                destinatario CHAR(40) NOT NULL,
                data_entrega DATE,
                tipo CHAR(20),
                funcionario CHAR(40)
            );
        """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.destinatario = self.nomed_entry.get()
        self.dataen = self.dataen_entry.get()
        self.tipo = self.tipo_entry.get()
        self.funcionario = self.nomef_entry.get()

    def onDoubleClick(self, event):
        self.limpa_tela()

        for n in self.listaEnc.selection():
            col1, col2, col3, col4, col5 = self.listaEnc.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nomed_entry.insert(END, col2)
            self.tipo_entry.insert(END, col3)
            self.dataen_entry.insert(END, col4)
            self.nomef_entry.insert(END, col5)

    def add_encomenda(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO Encomendas(
        codigo, destinatario, data_entrega, tipo, funcionario) VALUES(?, ?, ?, ?, ?)
        """, (self.codigo, self.destinatario, self.dataen, self.tipo, self.funcionario))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def deleta_encomenda(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE codigo = ? """, (self.codigo,))

        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def select_lista(self):
        self.listaEnc.delete(*self.listaEnc.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT codigo, destinatario, data_entrega, tipo, funcionario 
                   FROM Encomendas ORDER BY destinatario ASC; """)
        for i in lista:
            self.listaEnc.insert("", END, values=i)
        self.desconecta_bd()


class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        root.mainloop()

    def tela(self):
        self.root.title("Registro de Encomendas")
        self.root.configure(background='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        ### Criação do botao limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar", bd=2, bg='#107db2', fg='white'
                                , font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg='#107db2', fg='white'
                                , font=('verdana', 8, 'bold'))
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao novo
        self.bt_novo = Button(self.frame_1, text="Novo", bd=2, bg='#107db2', fg='white'
                              , font=('verdana', 8, 'bold'), command=self.add_encomenda)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=2, bg='#107db2', fg='white'
                                 , font=('verdana', 8, 'bold'))
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg='#107db2', fg='white'
                                , font=('verdana', 8, 'bold'), command=self.deleta_encomenda())
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text="Código", bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.14)

        # Criação da label e entrada do nome do destinatário
        self.lb_nomed = Label(self.frame_1, text='Destinatário(a)', bg='#ffffff', fg='black')
        self.lb_nomed.place(relx=0.05, rely=0.35)

        self.nomed_entry = Entry(self.frame_1)
        self.nomed_entry.place(relx=0.05, rely=0.45, relwidth=0.50)

        # Criação da label e entrada do tipo de encomenda
        self.lb_tipo = Label(self.frame_1, text='Tipo', bg='#ffffff', fg='black')
        self.lb_tipo.place(relx=0.6, rely=0.35)

        self.tipo_entry = Entry(self.frame_1)
        self.tipo_entry.place(relx=0.6, rely=0.45, relwidth=0.30)

        # Criação da label e entrada do nome do funcionário
        self.lb_nomef = Label(self.frame_1, text='Funcionário(a)', bg='#ffffff', fg='black')
        self.lb_nomef.place(relx=0.05, rely=0.60)

        self.nomef_entry = Entry(self.frame_1)
        self.nomef_entry.place(relx=0.05, rely=0.70, relwidth=0.50)

        # Criação da label e entrada da data entrada
        self.lb_dataen = Label(self.frame_1, text='Data Entrega', bg='#ffffff', fg='black')
        self.lb_dataen.place(relx=0.6, rely=0.60)

        self.dataen_entry = Entry(self.frame_1)
        self.dataen_entry.place(relx=0.6, rely=0.70, relwidth=0.30)

    def lista_frame2(self):
        self.listaEnc = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.listaEnc.heading('#0', text='ID')
        self.listaEnc.heading('#1', text='Código')
        self.listaEnc.heading('#2', text='Destinatário(a)')
        self.listaEnc.heading('#3', text='Data Entrega')
        self.listaEnc.heading('#4', text='Tipo')
        self.listaEnc.heading('#5', text='Funcionário(a)')

        self.listaEnc.column('#0', width=1)
        self.listaEnc.column('#1', width=100)
        self.listaEnc.column('#2', width=160)
        self.listaEnc.column('#3', width=70)
        self.listaEnc.column('#4', width=70)
        self.listaEnc.column('#5', width=150)

        self.listaEnc.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        self.scroolLista = ttk.Scrollbar(self.frame_2, orient='vertical')
        self.listaEnc.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)
        self.listaEnc.bind("<Double-1>", self.onDoubleClick)


Application()
