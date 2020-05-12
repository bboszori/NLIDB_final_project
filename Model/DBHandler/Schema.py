class Schema:
    connections = None
    tabledict = None
    rowDict = None
    keys = None

    def __init__(self, dbConn):
        cursor = dbConn.cursor()

        Schema.tabledict = dict()
        Schema.rowDict = dict()
        Schema.keys = dict()
        Schema.connections = dict()

        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        tablelist = cursor.fetchall()

        for item in tablelist:
            Schema.tabledict[item[0]] = dict()
            Schema.rowDict[item[0]] = dict()

            cursor.execute("select column_name, data_type from information_schema.columns where table_name = '%s'" % (item[0]))
            columnlist = cursor.fetchall()
            columntype = dict()
            columnvalues = dict()

            for column in columnlist:
                columntype[column[0]] = column[1]
                cursor.execute("SELECT %s FROM %s ORDER BY RANDOM() LIMIT 100" % (column[0], item[0]))
                row = cursor.fetchall()
                columnvalues[column[0]] = row

            Schema.tabledict[item[0]] = columntype
            Schema.rowDict[item[0]] = columnvalues

        for table in Schema.tabledict:
            cursor.execute("select column_name, data_type from information_schema.columns where (column_key = 'PRI') AND (table_name = '%s')" % (table))
            primkeys = cursor.fetchall()

            Schema.keys[table] = dict()
            keylist = list()

            for row in primkeys:
                keylist.append(row[0])

            Schema.keys[table] = keylist

        for table in Schema.tabledict:
            Schema.connections[table] = dict()

        cursor.execute("SELECT table_name, column_name, referenced_table_name, referenced_column_name from information_schema.key_column_usage where referenced_table_name is not null")
        forkeys = cursor.fetchall()

        for key in forkeys:
            table1 = forkeys[0]
            table2 = forkeys[2]

            if not table2 in Schema.connections[table1]:
                Schema.connections[table1].append(table2)
            if not table1 in Schema.connections[table2]:
                Schema.connections[table2].append(table1)

    def getJoinPath(self, table1, table2):
        if not (table1 in Schema.tabledict) or not (table2 in Schema.tabledict):
            return list()

        visited = dict()
        for table in Schema.tabledict:
            visited[table] = False

        prev = dict()
        queue = list()
        queue.append(table1)
        visited[table1] = True
        found = False

        while len(queue) != 0 and not found:
            tableCurr = queue[0]
            del queue[0]

            for tableNext in Schema.connections[tableCurr]:
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
        table1Keys = Schema.keys[table1]
        table2Keys = Schema.keys[table2]

        if table1Keys == table2Keys:
            return set()
        keys1ContainedIn2 = True

        for table1Key in table1Keys:
            if not table1Key in Schema.tabledict[table2]:
                keys1ContainedIn2 = False
                break

        if keys1ContainedIn2:
            return set(table1Keys)

        keys2ContainedIn1 = True
        for table2Key in table2Keys:
            if not table2Key in Schema.tabledict[table1]:
                keys2ContainedIn1 = False
                break

        if keys2ContainedIn1:
            return set(table2Keys)
        return set()

    def getTableNames(self):
        tableList = []
        for tableName in self.tabledict:
            tableList.append(tableName)
        return tableList

    def getColumns(self, table):
        columnList = []

        for column in self.tabledict[table]:
            columnList.append(column)

        return columnList

    def getValues(self, tableName, columnName):
        return self.rowDict[tableName][columnName]





