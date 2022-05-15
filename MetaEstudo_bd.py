from tkinter import *
from tkinter import ttk
import sqlite3

janela = Tk()


# comamdo limpa os campos
class Funcs:
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.assunto_entry.delete(0, END)
        self.edital_entry.delete(0, END)
        self.site_da_aula_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("estudos.bd")
        self.cursor = self.conn.cursor()
        print("conectando ao banco de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("desconectando ao banco de dados")

    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudos (
                cod INTEGER PRIMARY KEY,
                assunto CHAR(40) NOT NULL,
                edital INTEGER(20),
                site_da_aula CHAR(40)
            );
        """)
        self.conn.commit()
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.assunto = self.assunto_entry.get()
        self.edital = self.edital_entry.get()
        self.site_da_aula = self.site_da_aula_entry.get()

    def add_estudo(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO estudos (assunto, edital, site_da_aula )
        VALUES (?, ?, ?)""", (self.assunto, self.edital, self.site_da_aula))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT cod, assunto, edital, site_da_aula FROM estudos
            ORDER BY cod ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClic(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.assunto_entry.insert(END, col2)
            self.edital_entry.insert(END, col3)
            self.site_da_aula_entry.insert(END, col4)

    def deleta_estudo(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM estudos WHERE cod=? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_estudo(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE estudos SET assunto = ?, edital = ?, site_da_aula = ?
            WHERE cod = ?""", (self.assunto, self.edital, self.site_da_aula, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_assunto(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.assunto_entry.insert(END, '%')
        assunto = self.assunto_entry.get()
        self.cursor.execute(
            """SELECT cod, assunto, edital, site_da_aula FROM estudos
            WHERE assunto LIKE '%s' ORDER BY cod ASC""" % assunto)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()

class application(Funcs):
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame_2()
        self.montaTabelas()
        self.select_lista()
        janela.mainloop()

    # aqui é a tela principal

    def tela(self):
        self.janela.title("MetaEstudo")
        self.janela.configure(background='PowderBlue')
        self.janela.geometry("700x500")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=500, height=300)

    # os fremes sao os quadrados que dividem as telas maiores em tela menores
    def frames_da_tela(self):
        self.frame_1 = Frame(self.janela, bg='DodgerBlue', highlightbackground='MediumSlateBlue', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.janela, bg='DodgerBlue', highlightbackground='MediumSlateBlue', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.52, relwidth=0.96, relheight=0.46)

    # widgets é como são chamados os botoes
    def widgets_frame1(self):
        # criação dos botoes
        self.bt_limpar = Button(self.frame_1, text="limpar", bd=5, bg="DodgerBlue", fg="Honeydew",
                                font=("arial", 8, "bold"), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.1)

        # criação dos botoes
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=5, bg="DodgerBlue", fg="Honeydew",
                                font=("arial", 8, "bold"),command = self.busca_assunto)
        self.bt_buscar.place(relx=0.18, rely=0.72, relwidth=0.1, relheight=0.1)

        # criação dos botoes
        self.bt_Cadastrar = Button(self.frame_1, text="Cadastrar", bd=5, bg="DodgerBlue", fg="Honeydew",
                                   font=("arial", 8, "bold"), command=self.add_estudo)
        self.bt_Cadastrar.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.1)

        # criação dos botoes
        self.bt_Alterar = Button(self.frame_1, text="Alterar", bd=5, bg="DodgerBlue", fg="Honeydew",
                                 font=("arial", 8, "bold"), command=self.altera_estudo)
        self.bt_Alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.1)

        # criação dos botoes
        self.bt_Apagar = Button(self.frame_1, text="Apagar", bd=5, bg="DodgerBlue", fg="Honeydew",
                                font=("arial", 8, "bold"), command=self.deleta_estudo)
        self.bt_Apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.1)

        # criando label e as entradas
        self.lb_codigo = Label(self.frame_1, text="Codigo:", bg="DodgerBlue", fg="Honeydew", font=("arial", 8, "bold"))
        self.lb_codigo.place(relx=0.05, rely=0.01, relwidth=0.1, relheight=0.1)

        self.codigo_entry = Entry(self.frame_1,bg="white", fg="Black")
        self.codigo_entry.place(relx=0.05, rely=0.09, relwidth=0.1, relheight=0.1)

        self.lb_assunto = Label(self.frame_1, text="Assunto:", bg="DodgerBlue", fg="Honeydew",
                                font=("arial", 8, "bold"))
        self.lb_assunto.place(relx=0.05, rely=0.6, relwidth=0.1, relheight=0.1)

        self.assunto_entry = Entry(self.frame_1, bg="white", fg="Black")
        self.assunto_entry.place(relx=0.18, rely=0.6, relwidth=0.5, relheight=0.1)

        self.lb_edital = Label(self.frame_1, text="Nº no EDITAL:", bg="DodgerBlue", fg="Honeydew",
                               font=("arial", 8, "bold"))
        self.lb_edital.place(relx=0.7, rely=0.6, relwidth=0.1, relheight=0.1)

        self.edital_entry = Entry(self.frame_1, bg="white", fg="Black")
        self.edital_entry.place(relx=0.82, rely=0.6, relwidth=0.15, relheight=0.1)

        self.lb_site_da_aula = Label(self.frame_1, text="Site da Aula:", bg="DodgerBlue", fg="Honeydew",
                                     font=("arial", 8, "bold"))
        self.lb_site_da_aula.place(relx=0.05, rely=0.4, relwidth=0.1, relheight=0.1)

        self.site_da_aula_entry = Entry(self.frame_1, bg="white", fg="Black")
        self.site_da_aula_entry.place(relx=0.18, rely=0.4, relwidth=0.50, relheight=0.1)

    def lista_frame_2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,  columns=("col0", "col1", "col2", "col3",))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="COD")
        self.listaCli.heading("#2", text="Assunto")
        self.listaCli.heading("#3", text="Nº no EDITAL")
        self.listaCli.heading("#4", text="Site da Aula")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClic)


application()
