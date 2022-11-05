from modulos import *


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
        dicionario = {'cod': "Digite o Código", 'cod2': "", 'dest': "Digite o nome do Destinatário(a)", 'dest2': ""}

        if self.codigo_entry.get() in dicionario.values() or self.destinatario_entry.get() in dicionario.values():
            msg = "Os campos 'Código' e 'Destinatário(a)' são obrigatórios."
            messagebox.showinfo("AVISO", msg)
        else:
            self.conecta_bd()

            self.cursor.execute(""" INSERT INTO Encomendas (codigo, destinatario, data_entrada, tipo, funcionario) 
                VALUES (?, ?, ?, ?, ?)""",
                                (self.codigo, self.destinatario, self.dataentrada, self.tipo, self.funcionario))
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
        msg = messagebox.askyesno(title="Aviso", message="Tem certeza de que deseja apagar?")
        if msg:
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