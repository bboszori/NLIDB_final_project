from tkinter import *

class App(Frame):
    def __init__(self, root):
        self.text_color = '#4E598C'
        root.title('DataWiz')
        root.iconbitmap('icon.ico')
        Frame.__init__(self, root)
        self.pack(fill=BOTH, expand=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(4, weight=2)
        self.grid_rowconfigure(5, weight=1)


        self.title_frame = Frame(self, width=root.winfo_width()/4, height=50)
        self.title_frame.grid(column=0, row=0, sticky="nsew")

        self.myLabel = Label(self.title_frame,text="Data\nWiz",font=('Calibri',40, 'bold'), fg=self.text_color, padx=10,
                             pady=10)
        self.myLabel.pack()

        self.frame_db = LabelFrame(self, text= "Database connection", height=root.winfo_height()-50,
                  width=root.winfo_width()/4, padx=10, pady=10)
        self.frame_db.grid(column=0, row=1, rowspan=4, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        for i in range(10):
            self.frame_db.grid_rowconfigure(i, weight=1)

        self.question_frame = LabelFrame(self, text="Ask the question", height=100, width=root.winfo_width(
            )*0.75, padx=10, pady=10)
        self.question_frame.grid(column=1,row=0, sticky="nsew")


