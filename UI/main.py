from UI.Mainwindow import App
from tkinter import *

class DataWiz:
    def __init__(self):
        pass

    def startProgram(self):
      root = Tk()
      root.geometry("800x700")
      App(root)
      root.mainloop()