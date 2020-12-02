class Query:
    def __init__(self):
        self.__select = Select()
        self.__function = Function()
        self.__from = From()
        self.__join = Join()
        self.__where = Where()
        self.__groupby = Groupby()
        self.__orderby = Orderby()

    def sqlquerystring(self):
        pass


class Select:
    def __init__(self, columnlist = None, distinct = False):
        self.__distinct = distinct
        if columnlist == None:
            self.__columnlist = []
        else:
            self.__columnlist = columnlist

    @property
    def get_columnlist(self):
        return self.__columnlist

    @property
    def get_distinct(self):
        return self.__distinct

    def set_distinct(self, isdistinct):
        self.__distinct = isdistinct


    def addcolumn(self, column):
        if column not in self.__columnlist:
            self.__columnlist.append(column)

    def checkcolumn(self, column):
        if column in self.__columnlist:
            return True
        else:
            return False

class Function:
    def __init__(self, type=None, column=None):
        self.__type = type
        self.__column = column

    @property
    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    @property
    def get_column(self):
        return self.__column

    def set_column(self, column):
        self.__column = column

class From:
    def __init__(self, tablelist=None):
        if tablelist == None:
            self.__tablelist = []
        else:
            self.__tablelist = tablelist

    @property
    def get_tablelist(self):
        return self.__tablelist

    def addtable(self, table):
        if table not in self.__tablelist:
            self.__tablelist.append(table)

    def checktable(self, table):
        if table in self.__tablelist:
            return True
        else:
            return False

class Join:
    pass

class Where:
    def __init__(self, logicop=None):
        self.__conditionlist = None
        self.__logicop = logicop

    @property
    def get_conditionlist(self):
        return self.__conditionlist

    def addcondition(self, condition):
        if condition not in self.__conditionlist:
            self.__conditionlist.append(condition)

    @property
    def get_logicop(self):
        return self.__logicop

    def set_logicop(self, logicop):
        self.__logicop = logicop

class Condition:
    def __init__(self, column=None, op=None, value=None):
        self.__column = column
        self.__operator = op
        self.value = value

    @property
    def get_operator(self):
        return self.__operator

    def set_operator(self, op):
        self.__operator = op

    @property
    def get_column(self):
        return self.__column

    def set_column(self, column):
        self.__column = column

    @property
    def get_value(self):
        return self.__column

    def set_value(self, column):
        self.__column = column

class Groupby:
    def __init__(self, column=None):
        self.__column = column

    @property
    def get_column(self):
        return self.__column

    def set_column(self, column):
        self.__column = column

class Orderby:
    def __init__(self, type=None, column=None):
        self.__type = type
        self.__column = column

    @property
    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    @property
    def get_column(self):
        return self.__column

    def set_column(self, column):
        self.__column = column