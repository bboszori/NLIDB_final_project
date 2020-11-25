class Query:
    def __init__(self):
        self.__queryparts = dict()
        self.__blocks = list()

        self.__queryparts["SELECT"] = list()
        self.__queryparts["FROM"] = set()
        self.__queryparts["WHERE"] = set()

    def get(self):
        return Query.toString()

    def getComponent(self, keyWord):
        return list(self.__queryparts[keyWord])

    def add(self, key, value):
        if self.isSet(key):
            self.__queryparts[key].add(value)
        else:
            self.__queryparts[key].append(value)

    def addBlock(self, query):
        self.__blocks.append(query)
        SQLQuery.add(self, "FROM", "BLOCK%d" % len(self.__blocks))

    def isSet(self, key):
        if (key == "SELECT"):
            return False
        else:
            return True

    @staticmethod
    def toSBLine(SELECT):
        sb = []
        for val in SELECT:
            if len(sb) == 0:
                sb.append(val)
            else:
                sb.append(", ")
                sb.append(val)
        return ''.join(sb)

    @staticmethod
    def toSBLineCondition(WHERE):
        sb = []
        for val in WHERE:
            if len(sb) == 0:
                sb.append(val)
            else:
                sb.append(" AND ")
                sb.append(val)
        return ''.join(sb)

    def toString(self):
        if len(self.__queryparts["SELECT"]) == 0 or len(self.__queryparts["FROM"]) == 0:
            return "Illegal Query"

        sb = []
        for i in range(0, len(self.__blocks)):
            sb.append("BLOCK%d:\n" % (i + 1))
            sb.append("%s\n" % self.__blocks[i].toString())
            ''.join(sb)

        sb.append("SELECT ")
        sb.append("%s\n" % Query.toSBLine(self.__queryparts["SELECT"]))
        sb.append("FROM ")
        sb.append("%s\n" % Query.toSBLine(self.__queryparts["FROM"]))

        if len(self.__queryparts["WHERE"]) != 0:
            sb.append("WHERE ")
            sb.append("%s\n" % Query.toSBLineCondition(self.__queryparts["WHERE"]))

        sb.append(";\n")
        return ''.join(sb)