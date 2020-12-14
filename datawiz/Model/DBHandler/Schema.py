from datawiz.Model.DBHandler.Column import Column
from datawiz.Model.DBHandler.Table import Table

class Schema:

    def __init__(self, dbconn, dbname, dbtype='mysql'):

        self.__cursor = dbconn.cursor()
        self.__tables = []
        self.__rowDict = dict()
        self.__keys = dict()
        self.__connections = dict()
        self.__keypairs = dict()
        self.__dbName = dbname

        if dbtype == "mssql":
            self.retrieveMSQLTableInfo()
            self.retrieveMSQLKeyInfo()
            self.retrieveMSQLConnections()
        elif dbtype == "mysql":
            self.retrieveMySQLTableInfo()
            self.retrieveMySQLKeyInfo()
            self.retrieveMySQLConnections()
        else:
            raise AttributeError()

    def retrieveMSQLTableInfo(self):
        self.__cursor.execute(
            "SELECT TABLE_NAME FROM %s.information_schema.tables WHERE TABLE_TYPE='BASE TABLE'" % self.__dbName)
        tablelist = self.__cursor.fetchall()

        for item in tablelist:
            currTable = Table(item[0])
            self.__tables.append(currTable)

            self.__cursor.execute(
                "SELECT column_name, data_type from information_schema.columns where table_name = '%s'" % (
                    item[0]))
            columnlist = self.__cursor.fetchall()

            for column in columnlist:
                currColumn = Column(column[0], column[1])
                currTable.add_column(currColumn)
                self.__cursor.execute(
                    "SELECT %s FROM %s ORDER BY TABLESAMPLE(10 PERCENT)" % (column[0], item[0]))
                # cursor.execute("SELECT %s FROM %s ORDER BY RAND() LIMIT 100" % (column[0], item[0]))
                row = self.__cursor.fetchall()
                currColumn.set_samplevalues(row)

    def retrieveMySQLTableInfo(self):
        self.__cursor.execute(
            "SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = '%s';" %
            self.__dbName)
        tablelist = self.__cursor.fetchall()

        for item in tablelist:
            currTable = Table(item[0])
            self.__tables.append(currTable)

            self.__cursor.execute(
                "SELECT column_name, data_type from information_schema.columns where table_name = '%s'" % (
                    item[0]))
            columnlist = self.__cursor.fetchall()

            for column in columnlist:
                currColumn = Column(column[0],column[1])
                currTable.add_column(currColumn)
                self.__cursor.execute(
                    "SELECT %s FROM %s.%s ORDER BY RAND() LIMIT 10" % (column[0], self.__dbName,
                                                                        item[0]))
                row = self.__cursor.fetchall()
                currColumn.set_samplevalues(row)

    def retrieveMSQLKeyInfo(self):
        for table in self.__tables:
            self.__cursor.execute(
                "SELECT cu.COLUMN_NAME, cs.DATA_TYPE " + ("FROM %s "
                                                          ".INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
                                                          "as cu " % self.__dbName) + (
                        "INNER JOIN %s "
                        ".INFORMATION_SCHEMA.COLUMNS as cs "
                        % self.__dbName) + (
                    "ON cu.COLUMN_NAME=cs.COLUMN_NAME AND,cs.TABLE_NAME=cu.TABLE_NAME ") + (
                        "WHERE cs.TABLE_NAME = '%s' AND CONSTRAINT_NAME LIKE 'PK%s'" % (
                    table, '%')))
            primkeys = self.__cursor.fetchall()

            for item in primkeys:
                table.get_column(item[0]).setasPrimarykey()

    def retrieveMySQLKeyInfo(self):
        for table in self.__tables:
            self.__cursor.execute(
                "SELECT sc.COLUMN_NAME, cc.DATA_TYPE from information_schema.statistics as sc INNER JOIN "
                "INFORMATION_SCHEMA.COLUMNS as cc ON sc.TABLE_NAME = cc.TABLE_NAME AND sc.COLUMN_NAME = "
                "cc.COLUMN_NAME where sc.TABLE_SCHEMA = '%s' AND sc.INDEX_NAME = 'PRIMARY' AND sc.TABLE_NAME = '%s'"
                % (self.__dbName, table.get_tablename))
            primkeys = self.__cursor.fetchall()

            for item in primkeys:
                table.get_column(item[0]).setasPrimarykey()

    def retrieveMSQLConnections(self):
        self.__cursor.execute((
                "SELECT FK.TABLE_NAME, CU.COLUMN_NAME, PK.TABLE_NAME, PT.COLUMN_NAME FROM %s.INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS as C INNER JOIN %s.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as FK ON C.CONSTRAINT_NAME = FK.CONSTRAINT_NAME INNER JOIN %s.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as PK ON C.UNIQUE_CONSTRAINT_NAME = PK.CONSTRAINT_NAME INNER JOIN %s.INFORMATION_SCHEMA.KEY_COLUMN_USAGE as CU ON C.CONSTRAINT_NAME = CU.CONSTRAINT_NAME INNER JOIN ( SELECT i1.TABLE_NAME, i2.COLUMN_NAME FROM %s.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as i1 INNER JOIN %s.INFORMATION_SCHEMA.KEY_COLUMN_USAGE as i2 ON i1.CONSTRAINT_NAME = i2.CONSTRAINT_NAME WHERE i1.CONSTRAINT_TYPE = 'PRIMARY KEY') as PT ON PT.TABLE_NAME = PK.TABLE_NAME" % (
            self.__dbName, self.__dbName, self.__dbName, self.__dbName, self.__dbName, self.__dbName)))

        forkeys = self.__cursor.fetchall()

        for item in forkeys:
            currtable = self.gettablebyname(item[0])
            currtable.get_column(item[1]).add_foreign_key(item[2], item[3])

    def retrieveMySQLConnections(self):
        for tableName in self.getTableNames():
            self.__connections[tableName] = list()

        self.__cursor.execute("SELECT table_name, column_name, referenced_table_name, referenced_column_name from "
                             "information_schema.key_column_usage where referenced_table_name is not null AND "
                              "TABLE_SCHEMA = '%s'" % self.__dbName)

        forkeys = self.__cursor.fetchall()

        for item in forkeys:
            currtable = self.gettablebyname(item[0])
            currtable.add_foreign_key(item[1], item[2], item[3])

        for fk in forkeys:
            table1 = fk[0]
            table2 = fk[2]
            if not table2 in self.__connections[table1]:
                self.__connections[table1].append(table2)
            if not table1 in self.__connections[table2]:
                self.__connections[table2].append(table1)

            ts = table1 + "." + table2
            kp = table1 + "." + fk[1] + "=" + table2 + "." + fk[3]
            self.__keypairs[ts] = kp

    def getJoinPath(self, table1, table2):

        if not (table1 in self.__tables) or not (table2 in self.__tables):
            return list()

        visited = dict()
        for table in self.__tables:
            visited[table.get_tablename()] = False

        prev = dict()
        queue = list()
        queue.append(table1)
        visited[table1.get_tablename()] = True
        found = False

        while len(queue) != 0 and not found:
            tableCurr = queue[0]
            del queue[0]

            for tableNext in self.__connections[tableCurr]:
                if not visited[tableNext]:
                    visited[tableNext] = True
                    queue.append(tableNext)
                    prev[tableNext] = tableCurr
                if tableNext == table2:
                    found = True

        path = list()

        if visited[table2]:
            tableEnd = table2
            path.insert(0, tableEnd)
            while tableEnd in prev:
                tableEnd = prev[tableEnd]
                path.insert(0, tableEnd)
        return path

    def getJoinKeys(self, table1, table2):
        ts1 = table1 + "." + table2
        ts2 = table2 + "." + table1
        if ts1 in self.__keypairs:
            return "ON " + self.__keypairs[ts1]
        elif ts2 in self.__keypairs:
            return "ON " + self.__keypairs[ts2]
        else:
            return ""


    def isConnection(self,table1, table2):
        if (table2 in self.__connections[table1]) or (table1 in self.__connections[table2]):
            return True
        else:
            return False


    def getTablelist(self):
        return self.__tables

    def getTableNames(self):
        tableList = []
        for table in self.__tables:
            tableList.append(table.get_tablename)
        return tableList

    def gettablebyname(self, tname):
        for i in self.__tables:
            if i.get_tablename == tname:
                return i
