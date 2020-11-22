class Column:
    def __init__(self, name, type, primary=False, foreign=False, sample=None, references = None):
        self.__columnname = name
        self.__type = type
        self.__primary = primary
        self.__foreign = foreign

        if sample == None:
            self.__samplevalues = []
        else:
            self.__samplevalues = sample

        if references == None:
            self.__foreign_refs = dict()
        else:
            self.__foreign_refs = references

    @property
    def getName(self):
        return self.__columnname

    @property
    def getType(self):
        return self.__type

    @property
    def get_primary(self):
        return self.__primary

    @property
    def get_foreign(self):
        return self.__foreign

    @property
    def get_references(self):
        return self.__foreign_refs

    @property
    def get_samplevalues(self):
        return self.__samplevalues

    def setasPrimarykey(self):
        self.__primary = True

    def setasForeignkey(self, reftable, refcolumns):
        self.__foreign = True
        self.__foreign_refs[reftable] = refcolumns
