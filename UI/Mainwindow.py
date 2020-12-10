from tkinter import *
from tkinter import messagebox
from Controller.ProgControl import ProgControl
from UI.Schemawindow import Schemawindow

class App(Frame):
    def __init__(self, root):
        self.controller = ProgControl()
        self.text_color = '#4E598C'
        self.root = root
        Frame.__init__(self, root)
        self.initialize_user_interface()


    def initialize_user_interface(self):
        self.root.title('DataWiz')
        self.root.iconbitmap('icon.ico')
        self.pack(fill=BOTH, expand=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=3)
        self.grid_rowconfigure(4, weight=3)
        self.grid_rowconfigure(5, weight=3)
        self.grid_rowconfigure(6, weight=3)


        self.title_frame = Frame(self)
        self.title_frame.grid(column=0, row=0, sticky="nsew")

        self.myLabel = Label(self.title_frame,text="Data\nWiz",font=('Calibri',40, 'bold'), fg=self.text_color, padx=10,
                             pady=10)
        self.myLabel.pack()

        self.frame_db = LabelFrame(self, text= "Database connection", padx=10, pady=10)
        self.frame_db.grid(column=0, row=1, rowspan=6, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        for i in range(11):
            self.frame_db.grid_rowconfigure(i, weight=1)

        self.label_host = Label(self.frame_db, text="Host",font=('Calibri',12, 'bold'),
                                fg=self.text_color, padx=5, pady=5)
        self.label_host.grid(column=0,row=0, sticky="sw")
        self.text_host  = Entry(self.frame_db, font=('Calibri',12), fg=self.text_color)
        self.text_host.grid(row=1, sticky="nsew")

        self.label_dbname = Label(self.frame_db, text="Database name", font=('Calibri',12, 'bold'),
                                  fg=self.text_color, padx=5, pady=5)
        self.label_dbname.grid(column=0,row=2, sticky="sw")
        self.text_dbname  = Entry(self.frame_db, font=('Calibri',12), fg=self.text_color)
        self.text_dbname.grid(column=0, row=3, sticky="nsew")

        self.label_user = Label(self.frame_db, text="User", font=('Calibri',12, 'bold'),
                                fg=self.text_color, padx=5, pady=5)
        self.label_user.grid(column=0,row=4, sticky="sw")
        self.text_user  = Entry(self.frame_db, font=('Calibri',12), fg=self.text_color)
        self.text_user.grid(column=0, row=5, sticky="nsew")

        self.label_password = Label(self.frame_db, text="Password", font=('Calibri',12, 'bold'),
                                    fg=self.text_color, padx=5, pady=5)
        self.label_password.grid(column=0,row=6, sticky="sw")
        self.text_password  = Entry(self.frame_db, show="*", font=('Calibri',12), fg=self.text_color)
        self.text_password.grid(column=0, row=7, sticky="nsew")

        self.button_connect = Button(self.frame_db, text="Connect", font=('Calibri',14, 'bold'),
                                     fg=self.text_color, command=self.dbconnection)
        self.button_connect.grid(row=9, sticky="nsew")

        self.button_disconnect = Button(self.frame_db, text="Disonnect", font=('Calibri',14, 'bold'),
                                        fg=self.text_color, command=self.dbdisconnect)
        #self.button_disconnect.grid(row=10, sticky="nsew")
        self.button_disconnect.pack_forget()


        self.question_frame = LabelFrame(self, text="Ask the question", padx=10, pady=10)
        self.question_frame.grid(column=1,row=0, sticky="nsew")

        self.question_frame.grid_rowconfigure(0, weight=1)
        self.question_frame.grid_rowconfigure(1, weight=1)
        self.question_frame.grid_columnconfigure(0, weight=1)

        self.entry_question = Entry(self.question_frame, font=('Calibri',12), fg=self.text_color)
        self.entry_question.grid(row=0, sticky="nsew")

        self.button_translate = Button(self.question_frame, text="Translate question", padx=5, pady=5,
                                       font=('Calibri',14, 'bold'), fg=self.text_color, state="disabled",
                                       command=self.starttranslate)
        self.button_translate.grid(row=1, sticky="ne")

        self.frame_choices = LabelFrame(self, text="Mapping choices", padx=10, pady=10)
        self.frame_choices.grid(column=1, row=1, rowspan=3, sticky="nsew")

        self.frame_query = LabelFrame(self, text="Final query", padx=10, pady=10)
        self.frame_query.grid(column=1, row=4, sticky="nsew")

        self.frame_data = LabelFrame(self, text="Data", padx=10, pady=10)
        self.frame_data.grid(column=1, row=5, rowspan=2, sticky="nsew")

    def dbconnection(self):
        self.controller.host = self.text_host.get()
        self.controller.dbname = self.text_dbname.get()
        self.controller.user = self.text_user.get()
        self.controller.password = self.text_password.get()

        if self.controller.initDBConnention():
            self.button_disconnect.grid(row=10, sticky="nsew")
            self.button_connect.grid_forget()
            self.button_translate['state'] = 'normal'
            Schemawindow(self.root, self.controller.schema)
        else:
            messagebox.showerror("Connection error", "We can not connect to the database.")

    def dbdisconnect(self):
        self.controller.connection.closeconnection()
        self.button_disconnect.grid_forget()
        self.button_connect.grid(row=9, sticky="nsew")
        self.button_translate['state'] = 'disabled'

    def starttranslate(self):
        self.button_translate['state'] = 'disabled'
        question = self.entry_question.get()
        if self.controller.processQuestion(question):
            nodes = self.controller.nodelist
            choices = self.controller.choiceslist
            self.choicestext = []

            self.frame_choices.grid_columnconfigure(0,weight=1)
            self.frame_choices.grid_columnconfigure(1,weight=2)
            for i in range(len(nodes)+1):
                self.frame_choices.grid_rowconfigure(i, weight=1)

            self.labels = []
            self.dropdowns = []
            self.clicked = []

            for i in range(len(nodes)):
                key = nodes[i].getWord.get_text()
                choice = []
                for ch in choices[i]:
                    choice.append(ch.tostr())
                self.choicestext.append(choice)

                self.labels.append(Label(self.frame_choices, text=nodes[i].getWord.get_text()))
                self.labels[i].grid(column=0, row=i, sticky="e")
                self.clicked.append(StringVar())
                self.clicked[i].set(choice[0])
                self.dropdowns.append(OptionMenu(self.frame_choices, self.clicked[i], *self.choicestext[i]))
                self.dropdowns[i].grid(column=1, row=i, sticky="nsew")






