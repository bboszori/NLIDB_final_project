from tkinter import *
from tkinter.ttk import *


class Schemawindow(Toplevel):
    def __init__(self, root, schema):
        self.schema = schema
        super().__init__(root)
        self.title("Database schema")
        self.geometry("500x200")

        self.tree_frame = Frame(self)
        self.tree_frame.pack()

        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.schematree = Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
        self.schematree.pack()

        self.tree_scroll.config(command=self.schematree.yview)

        self.schematree['columns'] = ('table', 'column', 'key')
        self.schematree.column("#0", width=40, stretch=NO)
        self.schematree.column("table", width=200, anchor=W)
        self.schematree.column("column", width=200, anchor=W)
        self.schematree.column("key", width=60, anchor=W)

        self.schematree.heading("#0", text="Label", anchor=W)
        self.schematree.heading("table", text="Table name", anchor=W)
        self.schematree.heading("column", text="Column name", anchor=W)
        self.schematree.heading("key", text="Key", anchor=W)

        tables = self.schema.getTablelist()
        count = 0
        for i in range(len(tables)):
            tn = tables[i].get_tablename
            self.schematree.insert(parent='', index='end', iid=i, values=(tn, '', ''))
            count += 1
        for i in range(len(tables)):
            columns = tables[i].get_columnlist
            for j in range(len(columns)):
                cn = columns[j].getName
                k = ''
                if columns[j].get_primary:
                    k = 'PK'
                elif columns[j].get_foreign:
                    k = 'FK'
                self.schematree.insert(parent=i, index='end', iid=count, values=('', cn, k))
                count += 1
