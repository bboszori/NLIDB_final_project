from tkinter import *

bg_color = '#F9C784'
hl_color = '#FCAF58'
strong_hl_color = '#FF8C42'
text_color = '#4E598C'

master = Tk()
master.title('DataWiz')
master.iconbitmap('icon.ico')
master.state('zoomed')

main_frame = Frame(master)
main_frame.pack(fill=BOTH, expand=1)

main_canvas = Canvas(main_frame, bg=bg_color)
main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))


title_frame = Frame(main_canvas, width=master.winfo_width()/4, height=100, bg=bg_color,
                    highlightbackground="#FCAF58",  highlightcolor="#FCAF58",
                    highlightthickness=1)
title_frame.place(relx = 0.0, rely = 0.0, anchor ='nw')

MyLabel = Label(title_frame,text="DataWiz",font=('Calibri',50, 'bold'), fg=text_color, padx=5, pady=5, bg=bg_color)

MyLabel.place(x=0.0, y=0.0, anchor='nw')


frame_db = Frame(main_canvas, height=master.winfo_height()-100, width=master.winfo_width()/4)
frame_db.place(x=0.0, y=100, anchor ='nw')

question_frame = Frame(main_canvas, height=100, width=master.winfo_width()*0.75, padx=5, pady=5)
question_frame.place(x=master.winfo_width()/4, y=0.0, anchor='nw')





master.mainloop()
