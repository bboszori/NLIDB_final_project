from Model.DBHandler.Schema import Schema
class Query:
    def __init__(self, schema):
        self.schema = schema
        self.select = Select()
        self.function = Function()
        self.fromq = From()
        self.join = Join()
        self.where = Where()
        self.groupby = Groupby()
        self.orderby = Orderby()

    def sqlquerystring(self):
        ss = self.selectstring()
        fs = self.fromstring()
        ws = self.wherestring()
        gs = self.groupstring()
        os = self.orderstring()

        return ss + fs + ws + gs + os


    def selectstring(self):
        sn = "SELECT "
        if self.select.get_distinct:
            sn += "DISTINCT "
        if self.function.get_column != None:
            self.select.addcolumn(self.function.get_column)
        if len(self.select.get_columnlist) == 0:
            self.select.addcolumn("*")

        for c in self.select.get_columnlist:
            if c == self.function.get_column:
                self.select.get_columnlist.remove(c)
                c = self.function.get_type + "(" + self.function.get_column + ")"
                self.select.addcolumn(c)

        cl=''
        if len(self.select.get_columnlist) > 1:
            cl = ', '.join(self.select.get_columnlist)
        elif len(self.select.get_columnlist) == 1:
            cl = self.select.get_columnlist[0]

        sn += cl + " "

        return sn

    def fromstring(self):
        tables = self.fromq.get_tablelist
        fn = ""
        if len(tables) == 1:
            fn += "FROM " + tables[0]
        if len(tables) == 2:
            jk = self.schema.getJoinKeys(tables[0], tables[1])
            if jk == "":
                print('Failure')
            else:
                fn += "FROM " + tables[0] + " INNER JOIN " + tables[1] + " " + jk + " "
        else:
            print('Failure')

        return fn

    def wherestring(self):
        wn = "WHERE "
        if len(self.where.get_conditionlist) == 0:
            return ""
        if len(self.where.get_conditionlist) == 1:
            cond = self.where.get_conditionlist[0].get_condstr()
            wn += cond
        if len(self.where.get_conditionlist) == 2:
            cond1 = self.where.get_conditionlist[0].get_condstr()
            cond2 = self.where.get_conditionlist[1].get_condstr()
            wn += cond1 + " " + self.where.get_logicop + " " + cond2
        else:
            print('Failure')

        return wn

    def groupstring(self):
        gn = "GROUP BY "
        if self.groupby.get_column == None:
            return ""
        else:
            gn += self.groupby.get_column + " "
        return gn

    def orderstring(self):
        on = "ORDER BY "
        if self.orderby.get_column == None:
            return ""
        else:
            on += self.orderby.get_column + " " + self.orderby.get_type + " "
        return on


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
        self.__conditionlist = []
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

    def get_condstr(self):
        return self.__column + " " + self.__operator + " " + self.value

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