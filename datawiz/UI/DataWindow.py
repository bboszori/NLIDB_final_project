from tkinter import *
from pandastable import Table, TableModel

class Datawindow(Frame):
    def __init__(self, root, data):
        self.root = root
        Frame.__init__(self, root)
        self.pack(fill=BOTH, expand=1)

        self.data_frame = Frame(self)
        self.data_frame.pack(fill=BOTH,expand=1)
        self.table = pt = Table(self.data_frame, dataframe=data,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return