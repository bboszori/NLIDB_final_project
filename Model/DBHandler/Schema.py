class Schema:

    def __init__(self, dbconn, dbname):

        self._cursor = dbconn.cursor()
        self._tableDict = dict()
        self._rowDict = dict()
        self._keys = dict()
        self._connections = dict()
        self._dbName = dbname

        self.retrieveMSQLTableInfo()
        self.retrieveMSQLKeyInfo()
        self.retrieveMSQLConnections()


    def retrieveMSQLTableInfo(self):
        self._cursor.execute(
            """SELECT TABLE_NAME FROM %s.information_schema.tables WHERE TABLE_TYPE='BASE TABLE""" % self._dbName)
        # self.cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        tablelist = self._cursor.fetchall()

        for item in tablelist:
            self._tableDict[item[0]] = dict()
            self._rowDict[item[0]] = dict()

            self._cursor.execute(
                "SELECT column_name, data_type from information_schema.columns where table_name = '%s'" % (
                    item[0]))
            columnlist = self._cursor.fetchall()
            columntype = dict()
            columnvalues = dict()

            for column in columnlist:
                columntype[column[0]] = column[1]
                self._cursor.execute(
                    "SELECT %s FROM %s ORDER BY TABLESAMPLE(10 PERCENT)" % (column[0], item[0]))
                # cursor.execute("SELECT %s FROM %s ORDER BY RAND() LIMIT 100" % (column[0], item[0]))
                row = self._cursor.fetchall()
                columnvalues[column[0]] = row

            self._tableDict[item[0]] = columntype
            self._rowDict[item[0]] = columnvalues

    def retrieveMySQLTableInfo(self):
        self._cursor.execute(
            "SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = '%s';" %
            self._dbName)
        tablelist = self._cursor.fetchall()

        for item in tablelist:
            self._tableDict[item[0]] = dict()
            self._rowDict[item[0]] = dict()

            self._cursor.execute(
                "SELECT column_name, data_type from information_schema.columns where table_name = '%s'" % (
                    item[0]))
            columnlist = self._cursor.fetchall()
            columntype = dict()
            columnvalues = dict()

            for column in columnlist:
                columntype[column[0]] = column[1]
                self._cursor.execute(
                    "SELECT %s FROM %s.%s ORDER BY RAND() LIMIT 100" % (column[0], self._dbName,
                                                                        item[0]))
                row = self._cursor.fetchall()
                columnvalues[column[0]] = row

            self._tableDict[item[0]] = columntype
            self._rowDict[item[0]] = columnvalues


    def retrieveMSQLKeyInfo(self):
        for table in self._tableDict:
            self._cursor.execute(
                "SELECT cu.COLUMN_NAME, cs.DATA_TYPE " + ("FROM %s "
                                                          ".INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
                                                          "as cu " % self._dbName) + (
                        "INNER JOIN %s "
                        ".INFORMATION_SCHEMA.COLUMNS as cs "
                        % self._dbName) + (
                    "ON cu.COLUMN_NAME=cs.COLUMN_NAME AND,cs.TABLE_NAME=cu.TABLE_NAME ") + (
                        "WHERE cs.TABLE_NAME = '%s' AND CONSTRAINT_NAME LIKE 'PK%s'" % (
                                                table, '%')))
            primkeys = self._cursor.fetchall()

            self._keys[table] = dict()
            keylist = list()

            for row in primkeys:
                keylist.append(row[0])

            self._keys[table] = keylist

    def retrieveMSQLConnections(self):
        for table in self._tableDict:
            self._connections[table] = dict()

        self._cursor.execute(
            "SELECT FK.TABLE_NAME, CU.COLUMN_NAME, PK.TABLE_NAME, PT.COLUMN_NAME" + (
                        "FROM %s.INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS as C" % self._dbName) + (
                        "INNER JOIN %s.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as FK ON C.CONSTRAINT_NAME = FK.CONSTRAINT_NAME" % self._dbName) + (
                        "INNER JOIN %s.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as PK ON C.UNIQUE_CONSTRAINT_NAME = PK.CONSTRAINT_NAME" % self._dbName) + (
                        "INNER JOIN %s.INFORMATION_SCHEMA.KEY_COLUMN_USAGE as CU ON C.CONSTRAINT_NAME = CU.CONSTRAINT_NAME" % self._dbName) + (
                        "INNER JOIN ( SELECT i1.TABLE_NAME, i2.COLUMN_NAME FROM %s.INFORMATION_SCHEMA.TABLE_CONSTRAINTS as i1" % self._dbName) + (
                        "INNER JOIN %s.INFORMATION_SCHEMA.KEY_COLUMN_USAGE as i2 ON i1.CONSTRAINT_NAME = i2.CONSTRAINT_NAME" % self._dbName) + (
                "WHERE i1.CONSTRAINT_TYPE = 'PRIMARY KEY') as PT ON PT.TABLE_NAME = PK.TABLE_NAME"))
        # self.cursor.execute("SELECT table_name, column_name, referenced_table_name,
        # referenced_column_name from information_schema.key_column_usage where referenced_table_name is not null" % (self._dbName, self.dbName, table))

        forkeys = self._cursor.fetchall()

        for key in forkeys:
            table1 = key[0]
            table2 = key[2]

            if table2 not in self._connections[table1]:
                self._connections[table1].append(table2)
            if table1 not in self._connections[table2]:
                self._connections[table2].append(table1)

    def getJoinPath(self, table1, table2):

        if not (table1 in self._tableDict) or not (table2 in self._tableDict):
            return list()

        visited = dict()
        for table in self._tableDict:
            visited[table] = False

        prev = dict()
        queue = list()
        queue.append(table1)
        visited[table1] = True
        found = False

        while len(queue) != 0 and not found:
            tableCurr = queue[0]
            del queue[0]

            for tableNext in self._connections[tableCurr]:
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
        table1Keys = self._keys[table1]
        table2Keys = self._keys[table2]

        if table1Keys == table2Keys:
            return set()
        keys1ContainedIn2 = True

        for table1Key in table1Keys:
            if table1Key not in self._tableDict[table2]:
                keys1ContainedIn2 = False
                break

        if keys1ContainedIn2:
            return set(table1Keys)

        keys2ContainedIn1 = True
        for table2Key in table2Keys:
            if table2Key not in self._tableDict[table1]:
                keys2ContainedIn1 = False
                break

        if keys2ContainedIn1:
            return set(table2Keys)
        return set()

    def getTableNames(self):
        tableList = []
        for tableName in self._tableDict:
            tableList.append(tableName)
        return tableList

    def getColumns(self, table):
        columnList = []

        for column in self._tableDict[table]:
            columnList.append(column)

        return columnList

    def getValues(self, tableName, columnName):
        return self._rowDict[tableName][columnName]
