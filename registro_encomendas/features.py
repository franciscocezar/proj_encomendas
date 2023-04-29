from modules import *


class Funcs:
    def __init__(self):
        self.listaEntregues = None
        self.listaEnc = None
        self.dataentrada_entry = None
        self.funcionario_entry = None
        self.retirada_entry = None
        self.destinatario_entry = None
        self.codigo_entry = None
        self.tipo_entry = None

    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.destinatario_entry.delete(0, END)
        self.tipo_entry.delete(0, END)
        self.funcionario_entry.delete(0, END)
        self.retirada_entry.delete(0, END)
        self.dataentrada_entry.delete(0, END)

    def conecta_bd(self):
        # self.conn = sqlite3.connect('registro_encomendas/database_name.db')
        self.conn = mysql.connector.connect(
                                            host='<localhost>',
                                            user='<root>',
                                            password='<password>',
                                            database='<database>')
        self.cursor = self.conn.cursor()
        print('Conectando ao banco de dados')

    def desconecta_bd(self):
        self.conn.close()
        print('Desconectando ao banco de dados')

    def montaTabelas(self):
        self.conecta_bd()

        self.quarentenabd = self.cursor.execute(
            """
         CREATE TABLE IF NOT EXISTS Quarentena(
                codigo VARCHAR(40) PRIMARY KEY,
                destinatario VARCHAR(40) NOT NULL,
                data_entrada VARCHAR(30) NOT NULL,
                tipo VARCHAR(20) NOT NULL,
                funcionario VARCHAR(40) NOT NULL,
                data_retirada VARCHAR(30) DEFAULT NULL,
                retirada_por VARCHAR(40) DEFAULT NULL
                );"""
        )
        self.conn.commit()
        print('Bando de dados criado')
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get().upper().strip()
        self.destinatario = self.destinatario_entry.get().title().strip()
        self.tipo = self.tipo_entry.get().title()
        self.funcionario = self.funcionario_entry.get().title()
        self.dataentrada = datetime.now().strftime('%d/%m/%Y %H:%M')

        self.retirada_por = self.retirada_entry.get().title()
        self.data_retirada = datetime.now().strftime('%d/%m/%Y %H:%M')

    def OnDoubleClick(self, event):

        self.limpa_tela()
        for n in self.listaEnc.selection():
            col1, col2, col3, col4, col5 = self.listaEnc.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.destinatario_entry.insert(END, col2)
            self.dataentrada_entry.insert(END, col3)
            self.tipo_entry.insert(END, col4)
            self.funcionario_entry.insert(END, col5)

    def SecondDoubleClick(self, event):
        self.limpa_tela()

        for n in self.listaEntregues.selection():
            col1, col2, col3, col4 = self.listaEntregues.item(n, 'values')
            self.destinatario_entry.insert(END, col1)
            self.dataentrada_entry.insert(END, col2)
            self.retirada_entry.insert(END, col3)
            self.codigo_entry.insert(END, col4)


    def add_encomenda(self):
        _regex = re.compile(r'[A-z0-9]{4,30}')
        self.conecta_bd()
        self.variaveis()
        self.cursor.execute(f"""SELECT codigo FROM Quarentena""")
        checagem = self.cursor.fetchall()
        check_lista = [cod[0] for cod in checagem]
        if self.codigo in check_lista:
            msg3 = """Este código já foi cadastrado."""
            messagebox.showinfo(title='AVISO', message=msg3)
        else:
            if not _regex.findall(self.codigo) or not _regex.findall(self.destinatario):
                msg = """Campos 'Código' e 'Destinatário(a)' são obrigatórios 
                ou foram preenchidos incorretamente."""
                messagebox.showinfo(title='AVISO', message=msg)

            else:
                self.cursor.execute(
                    f""" INSERT INTO Quarentena (codigo, destinatario, data_entrada, tipo, funcionario) 
                                        VALUES ("{self.codigo}", "{self.destinatario}", 
                                            "{self.dataentrada}", "{self.tipo}", "{self.funcionario}")""")

                self.conn.commit()
                self.select_lista()
                self.limpa_tela()
        self.desconecta_bd()

    def add_saida(self):
        self.variaveis()

        if not self.retirada_entry.get():
            msg = 'Informe a pessoa que retirou a encomenda.'
            messagebox.showinfo(title='AVISO', message=msg)
        else:
            msg = messagebox.askyesno(
                title='Aviso',
                message='Os dados estão corretos?',
                icon='warning',
            )
            if msg:
                self.conecta_bd()

                self.cursor.execute(
                    f"""UPDATE Quarentena 
                        SET data_retirada = "{self.data_retirada}", 
                            retirada_por = "{self.retirada_por}" 
                        WHERE codigo = "{self.codigo}" """)

                self.conn.commit()
                self.desconecta_bd()
                self.select_lista2()
                self.select_lista()
                self.limpa_tela()

    def altera_dados(self):
        self.variaveis()

        self.conecta_bd()
        self.cursor.execute(
            f"""UPDATE Quarentena 
                SET codigo = "{self.codigo}", destinatario = "{self.destinatario}", 
                    data_entrada = "{self.dataentrada}", tipo = "{self.tipo}", 
                    funcionario = "{self.funcionario}"
                WHERE codigo = "{self.codigo}" """)
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def deleta_encomenda(self):
        self.variaveis()
        msg = messagebox.askyesno(
            title='Aviso',
            message='Tem certeza de que deseja apagar?',
            icon='warning',
        )
        if msg:
            self.conecta_bd()

            self.cursor.execute(
                f""" DELETE FROM Quarentena WHERE codigo = "{self.codigo}" """)

            self.conn.commit()

            self.desconecta_bd()
            self.select_lista2()
            self.select_lista()
            self.limpa_tela()

    def select_lista(self):

        self.listaEnc.delete(*self.listaEnc.get_children())
        self.conecta_bd()
        self.cursor.execute(
            """ SELECT * FROM Quarentena
                ORDER BY data_entrada ASC; """)

        lista = self.cursor.fetchall()
        count = 0
        for i in lista:
            if i[6] is None:
                if count % 2 == 0:
                    self.listaEnc.insert(
                        '', END, values=[i[0], i[1], i[2], i[3], i[4]], iid=count, tag=('evenrow',)
                    )
                else:
                    self.listaEnc.insert(
                        '', END, values=[i[0], i[1], i[2], i[3], i[4]], iid=count, tag=('oddrow',)
                    )
                count += 1

        self.desconecta_bd()

    def select_lista2(self):
        self.listaEntregues.delete(*self.listaEntregues.get_children())
        self.conecta_bd()
        self.cursor.execute(
            """ SELECT * FROM Quarentena
                ORDER BY data_retirada DESC; """
        )
        lista = self.cursor.fetchall()
        count = 0
        for i in lista:
            if i[6] is not None:
                if count % 2 == 0:
                    self.listaEntregues.insert(
                        '', END, values=[i[1], i[5], i[6], i[0]], iid=count, tag=('evenrow',)
                    )
                else:
                    self.listaEntregues.insert(
                        '', END, values=[i[1], i[5], i[6], i[0]], iid=count, tag=('oddrow',)
                    )
                count += 1

        self.desconecta_bd()

    def busca_encomenda(self):
        self.conecta_bd()
        self.listaEnc.delete(*self.listaEnc.get_children())
        self.listaEntregues.delete(*self.listaEntregues.get_children())

        nome = self.destinatario_entry.get()
        codigo = self.codigo_entry.get()
        tipo = self.tipo_entry.get()
        funcionario = self.funcionario_entry.get()
        data = ''.join(self.dataentrada_entry.get().split('/'))

        self.cursor.execute(
            f"""
                            SELECT codigo, destinatario, data_entrada, tipo, funcionario 
                            FROM Quarentena
                            WHERE codigo LIKE '%{codigo}%' AND destinatario LIKE '%{nome}%' AND tipo LIKE '%{tipo}%'
                            AND funcionario LIKE '%{funcionario}%' AND data_entrada LIKE '%{data}%'
                            ORDER BY destinatario ASC"""
        )

        buscanomeEnc = self.cursor.fetchall()

        for i in buscanomeEnc:
            self.listaEnc.insert('', END, values=i)
            self.listaEntregues.insert('', END, values=i)

        self.limpa_tela()
        self.desconecta_bd()

    def self_destruction(self):
        self.conecta_bd()
        self.cursor.execute("SELECT data_entrada FROM Quarentena;")
        for date in self.cursor.fetchall():
            datetime_format = datetime.strptime(date[0][:10], '%d/%m/%Y')
            thirty_more_days = datetime_format + timedelta(30)
            if thirty_more_days < datetime.now():
                date_str_format = datetime_format.strftime('%d/%m/%Y')
                end_time = f'DELETE FROM Quarentena WHERE data_entrada LIKE "%{date_str_format}%"'
                self.cursor.execute(end_time)
                self.conn.commit()
        self.desconecta_bd()

