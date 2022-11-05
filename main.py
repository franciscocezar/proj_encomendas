from modulos import *
from frameGrad import GradientFrame
from reports import Relatorios
from funcionalidades import Funcs
from entPlaceHold import EntPlaceHold

root = Tk()


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

    def center(self, win):
        # :param win: the main window or Toplevel window to center

        # Apparently a common hack to get the window size. Temporarily hide the
        # window to avoid update_idletasks() drawing the window in the wrong
        # position.
        win.update_idletasks()  # Update "requested size" from geometry manager

        # define window dimensions width and height
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width

        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width

        # Get the window position from the top dynamically as well as position from left or right as follows
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2

        # this is the line that will center your window
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        win.deiconify()

    def tela(self):
        self.root.title("Registro de Encomendas")
        self.root.configure(bg='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        # self.root.maxsize(width=900, height=700)
        self.root.attributes('-alpha', 0.0)
        self.root.minsize(800, 600)
        self.center(self.root)
        self.root.attributes('-alpha', 1.0)

    def frames_da_tela(self):
        self.frame_1 = GradientFrame(self.root,
                                     highlightbackground='black', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = GradientFrame(self.root, highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # Botão Limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar", bd=1, bg='#107db2', fg='black',
                                font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=1, bg='#107db2', fg='black',
                                font=('verdana', 8, 'bold'), command=self.busca_encomenda)
        self.bt_buscar.place(relx=0.4, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão Novo
        self.bt_novo = Button(self.frame_1, text="Novo", bd=1, bg='#107db2', fg='black',
                              font=('verdana', 8, 'bold'), command=self.add_encomenda)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=1, bg='#107db2', fg='black',
                                 font=('verdana', 8, 'bold'), command=self.altera_dados)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=1, bg='#107db2', fg='black'
                                , font=('verdana', 8, 'bold'), command=self.deleta_encomenda)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        '''Entrada de Dados'''
        # Entrada ID
        self.id_entry = Entry(self.frame_1)
        self.id_entry.place(relx=0.53, rely=0.1, relwidth=0.03, relheight=0.08)

        # Label e Entrada Codigo
        self.lb_codigo = Label(self.frame_1, text="Código", bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = EntPlaceHold(self.frame_1, 'Digite o Código')
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.20)

        # Label e Entrada Destinatário

        # self.lb_destinatario = Label(self.frame_1, text="Destinatário(a)", bg='#dfe3ee', fg='#107db2')
        # self.lb_destinatario.place(relx=0.05, rely=0.35)

        self.destinatario_entry = EntPlaceHold(self.frame_1, 'Digite o nome do Destinatário(a)')
        self.destinatario_entry.place(relx=0.05, rely=0.45, relwidth=0.5)

        # Label e Entrada Tipo de Encomenda
        self.lb_tipo = Label(self.frame_1, text="Tipo", bg='#dfe3ee', fg='#107db2')
        self.lb_tipo.place(relx=0.6, rely=0.35)

        self.tipo_entry = EntPlaceHold(self.frame_1, 'Digite o Tipo de Encomenda')
        self.tipo_entry.place(relx=0.6, rely=0.45, relwidth=0.30)

        # Label e Entrada Funcionário
        self.lb_funcionario = Label(self.frame_1, text="Funcionário(a)", bg='#dfe3ee', fg='#107db2')
        self.lb_funcionario.place(relx=0.05, rely=0.6)

        self.lt_funcs = ['Francisco Junior', 'Jonas Santos', 'Rosana Silva']
        self.funcionario_entry = ttk.Combobox(self.frame_1, values=self.lt_funcs)
        self.funcionario_entry.place(relx=0.05, rely=0.7, relwidth=0.2)

        # Label e Entrada Data
        self.lb_dataentrada = Label(self.frame_1, text="Data de Entrada", bg='#dfe3ee', fg='#107db2')
        self.lb_dataentrada.place(relx=0.6, rely=0.6)

        self.dataentrada_entry = Entry(self.frame_1)
        self.dataentrada_entry.place(relx=0.6, rely=0.7, relwidth=0.3)

    def lista_frame2(self):
        # Abas
        self.abas = ttk.Notebook(self.frame_2)
        self.aba1 = GradientFrame(self.abas)
        self.aba2 = GradientFrame(self.abas)

        # self.aba1.configure(background='#e6e6fa')
        # self.aba2.configure(background='#a3aece')

        self.abas.add(self.aba1, text="Pendentes")
        self.abas.add(self.aba2, text="Entregues")

        self.abas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.listaEnc = ttk.Treeview(self.aba1, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6"))
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

        self.scrollLista = Scrollbar(self.aba1, orient='vertical')
        self.listaEnc.configure(yscrollcommand=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)
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





# root.attributes('-alpha', 0.0) # Opcional, para deixar a janela totalmente transparente até os ajustes serem feitos.
# root.minsize(750, 600)
# center(root) # A função
#
# root.attributes('-alpha', 1.0) # A interface fica visível novamente.

Application()
