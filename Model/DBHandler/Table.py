from .Column import Column

class Table:
    def __init__(self, name, columns=None):
        self.__tablename = name

        if columns == None:
            self.__columnlist = []
        else:
            self.__columnlist = columns

    @property
    def get_tablename(self):
        return self.__tablename

    @property
    def get_columnlist(self):
        return self.__columnlist

    def get_nr_of_columns(self):
        return len(self.__columnlist)

    def get_column(self, column_name):
        for column in self.__columnlist:
            if column_name == column.getName:
                return column

    def contains_column(self, column_name):
        for column in self.__columnlist:
            if column_name == column.getName:
                return True
        return False

    def add_column(self, column):
        self.__columnlist.append(column)

    def get_primarykeys(self):
        primary_keys = []
        for column in self.__columnlist:
            if column.get_primary():
                primary_keys.append(column)
        return primary_keys

    def add_primary_key(self, pk):
        for column in self.__columnlist:
            if column.getName == pk:
                column.setasPrimarykey()

    def get_foreign_keys(self):
        foreign_keys = []
        for column in self.__columnlist:
            if column.get_foreign():
                foreign_keys.append(column)
        return foreign_keys

    def add_foreign_key(self, column_name, foreign_table, foreign_column):
        for column in self.__columnlist:
            if column.getName == column_name:
                column.setasForeignkey(foreign_table,foreign_column)
