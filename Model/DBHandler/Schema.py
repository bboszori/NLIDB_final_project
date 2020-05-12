class Schema:
    connection = None
    tables = None
    tableRows = None
    keys = None

    def __init__(self, dbConn):
        cursor = dbConn.cursor()

        tabledict = dict()
        rowDict = dict()

        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public'""")
        tablelist = cursor.fetchall()

        for item in tablelist:
            tabledict[item[0]] = dict()
            rowDict[item[0]] = dict()

            cursor.execute("select column_name, data_type from information_schema.columns where table_name = '%s'" % (item[0]))
            columnlist = cursor.fetchall()
            columntype = dict()
            columnvalues = dict()

            for column in columnlist:
                columntype[column[0]] = column[1]
                cursor.execute("SELECT %s FROM %s ORDER BY RANDOM() LIMIT 100" % (column[0], item[0]))
                row = cursor.fetchall()
                columnvalues[column[0]] = row



    def gettingPrimarykeys(self):
        # TODO
        pass