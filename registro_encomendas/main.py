from entriesValidators import Validators
from frameGrad import GradientFrame
from features import Funcs
from modules import *
from reports import Relatorios

root = Tk()


class Application(Funcs, Relatorios, Validators):
    def __init__(self):
        super().__init__()
        self.frame_1 = None
        self.frame_2 = None
        self.root = root
        self.validateEntries()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.self_destruction()
        self.select_lista()
        self.select_lista2()
        self.Menus()
        root.mainloop()

    def center(self):
        APP_WIDTH = 350
        APP_HEIGHT = 320

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        app_center_coordinate_x = (screen_width / 3.5) - (APP_WIDTH / 3.5)
        app_center_coordinate_y = (screen_height / 4) - (APP_HEIGHT / 4)

        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{int(app_center_coordinate_x)}+{int(app_center_coordinate_y)}")

    def tela(self):
        self.root.title('Registro de Encomendas')
        self.root.configure(bg='gray20')
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.attributes('-alpha', 0.0)
        self.root.minsize(800, 600)
        self.center()
        self.root.attributes('-alpha', 1.0)

    def frames_da_tela(self):
        self.frame_1 = atk.Frame3d(self.root)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = atk.Frame3d(self.root)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):

        self.bt_limpar = atk.Button3d(
            self.frame_1, text='Limpar', command=self.limpa_tela
        )
        self.bt_limpar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_limpar, 'Limpar Campos')

        self.bt_buscar = atk.Button3d(
            self.frame_1, text='Buscar', command=self.busca_encomenda
        )
        self.bt_buscar.place(relx=0.41, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_buscar, 'Buscar por Nome')

        self.bt_novo = atk.Button3d(
            self.frame_1, text='Novo', command=self.add_encomenda
        )
        self.bt_novo.place(relx=0.63, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_novo, 'Registar Nova Encomenda')

        self.bt_alterar = atk.Button3d(
            self.frame_1, text='Alterar', command=self.altera_dados
        )
        self.bt_alterar.place(
            relx=0.74, rely=0.1, relwidth=0.1, relheight=0.15
        )
        atk.tooltip(self.bt_alterar, 'Alterar Dados')

        self.bt_apagar = atk.Button3d(
            self.frame_1, text='Apagar', command=self.deleta_encomenda
        )
        self.bt_apagar.place(relx=0.85, rely=0.1, relwidth=0.1, relheight=0.15)
        atk.tooltip(self.bt_apagar, 'Exclui Registro')

        """Entrada de Dados"""

        self.lb_codigo = Label(
            self.frame_1, text='Código', bg='gray20', fg='white'
        )
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.20)

        self.lb_destinatario = Label(
            self.frame_1, text='Destinatário(a)', bg='gray20', fg='white'
        )
        self.lb_destinatario.place(relx=0.05, rely=0.35)

        self.destinatario_entry = Entry(self.frame_1)
        self.destinatario_entry.place(relx=0.05, rely=0.45, relwidth=0.5)

        self.lb_tipo = Label(
            self.frame_1, text='Tipo', bg='gray20', fg='white'
        )
        self.lb_tipo.place(relx=0.6, rely=0.35)

        self.tipo_entry = Entry(self.frame_1)
        self.tipo_entry.place(relx=0.5970, rely=0.45, relwidth=0.306)

        self.lb_funcionario = Label(
            self.frame_1, text='Funcionário(a)', bg='gray20', fg='white'
        )
        self.lb_funcionario.place(relx=0.05, rely=0.6)

        self.lt_funcs = ['Francisco Junior', 'Jonas Santos', 'Rosana Silva']
        self.funcionario_entry = ttk.Combobox(
            self.frame_1, values=self.lt_funcs
        )
        self.funcionario_entry.place(relx=0.05, rely=0.7, relwidth=0.2)

        self.lb_dataentrada = Label(
            self.frame_1, text='Data:', bg='gray20', fg='white'
        )

        self.dataentrada_entry = Entry(
            self.frame_1, validate='key', validatecommand=self.valid
        )

        self.lb_retirada = LabelFrame(self.frame_1, text='Retirado por')
        self.lb_retirada.place(
            relx=0.6, rely=0.59, relwidth=0.3, relheight=0.35
        )

        self.retirada_entry = Entry(self.lb_retirada)
        self.retirada_entry.place(relx=0.05, rely=0.03, relwidth=0.90)

        self.bt_reti = atk.Button3d(
            self.lb_retirada, text='Confirmar', command=self.add_saida
        )
        self.bt_reti.place(relx=0.06, rely=0.43, relwidth=0.37, relheight=0.53)

    def lista_frame2(self):
        # Abas
        self.abas = ttk.Notebook(self.frame_2)
        self.abas.place(relx=0.01, rely=0.02, relwidth=0.96, relheight=0.962)

        self.aba1 = GradientFrame(self.abas)


        self.abas.add(self.aba1, text='Pendentes')

        #  *** ABA PENDENTES ***
        style = ttk.Style()
        style.configure(
            'Treeview',
            background='gray20',
            foreground='white',
            rowheight=25,
            fielbackground='gray20',
        )

        style.map(
            'Treeview',
            background=[('selected', 'white')],
            foreground=[('selected', 'black')],
        )

        self.listaEnc = ttk.Treeview(
            self.aba1,
            height=3,
            columns=('col1', 'col2', 'col3', 'col4', 'col5'),
            selectmode='extended',
        )
        self.listaEnc.heading('#0', text='',)
        self.listaEnc.heading('#1', text='Código')
        self.listaEnc.heading('#2', text='Destinatário(a)')
        self.listaEnc.heading('#3', text='Data Entrada')
        self.listaEnc.heading('#4', text='Tipo')
        self.listaEnc.heading('#5', text='Funcionário(a)')

        self.listaEnc.column('#0', width=0, stretch=NO)
        self.listaEnc.column('#1', width=90, anchor='center')
        self.listaEnc.column('#2', width=110, anchor='center')
        self.listaEnc.column('#3', width=80, anchor='center')
        self.listaEnc.column('#4', width=70, anchor='center')
        self.listaEnc.column('#5', width=70, anchor='center')

        # Cor da linha sem estar selecionada
        self.listaEnc.tag_configure('oddrow', background='gray20')
        self.listaEnc.tag_configure('evenrow', background='gray10')

        self.listaEnc.place(relx=0, rely=0.01, relwidth=0.97, relheight=0.97)

        self.scrollLista = Scrollbar(self.aba1, orient='vertical')
        self.listaEnc.configure(yscrollcommand=self.scrollLista.set)
        self.scrollLista.place(
            relx=0.97, rely=0.01, relwidth=0.025, relheight=0.97
        )
        self.listaEnc.bind('<Double-1>', self.OnDoubleClick)

        # *** ABA ENTREGUES ***
        self.aba2 = GradientFrame(self.abas)
        self.abas.add(self.aba2, text='Entregues')

        self.listaEntregues = ttk.Treeview(
            self.aba2,
            height=3,
            columns=('col1', 'col2', 'col3'),
            selectmode='extended',
        )
        self.listaEntregues.heading(
            '#0',
            text='',
        )

        self.listaEntregues.heading('#1', text='Destinatário(a)')
        self.listaEntregues.heading('#2', text='Data Retirada')
        self.listaEntregues.heading('#3', text='Retirada por')

        self.listaEntregues.column('#0', width=0, stretch=NO)
        self.listaEntregues.column('#1', width=80, anchor='center')
        self.listaEntregues.column('#2', width=70, anchor='center')
        self.listaEntregues.column('#3', width=70, anchor='center')

        # Cor da linha sem estar selecionada
        self.listaEntregues.tag_configure('oddrow', background='gray20')
        self.listaEntregues.tag_configure('evenrow', background='gray10')

        self.listaEntregues.place(
            relx=0, rely=0.01, relwidth=0.97, relheight=0.97
        )

        self.scrollLista2 = Scrollbar(self.aba2, orient='vertical')
        self.listaEntregues.configure(yscrollcommand=self.scrollLista2.set)
        self.scrollLista2.place(
            relx=0.97, rely=0.01, relwidth=0.025, relheight=0.97
        )
        self.listaEntregues.bind('<Double-1>', self.SecondDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit():
            self.root.destroy()

        menubar.add_cascade(label='Opções', menu=filemenu)
        menubar.add_cascade(label='Relatórios', menu=filemenu2)

        filemenu.add_command(label='Sair', command=Quit)
        filemenu.add_command(label='Limpar', command=self.limpa_tela)

        filemenu2.add_command(
            label='Dados Encomenda', command=self.geraRelatEncomenda
        )

    def validateEntries(self):
        self.valid = (self.root.register(self.dateValidator), '%P')


Application()
