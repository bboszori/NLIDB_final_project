class Column:
    def __init__(self, name, type, primary=False, foreign=False):
        self.__name = name
        self.__type = type
        self.__primary = primary
        self.__foreign = foreign

    @property
    def getName(self):
        return self.__name

    @property
    def getType(self):
        return self.__type

    @property
    def get_primary(self):
        return self.__primary

    def setasPrimarykey(self):
        self.__primary = True

    def setasForeignkey(self):
        self.__foreign = True
