import spacy
from .SQLComponent import SQLComponent

class Mapper:
    def __init__(self, nlp):
        self.__components = dict()
        self.__langparser = nlp

        f = open("keywords.csv", "r")
        while (True):
            line = f.readline()
            if not line:
                break
            nodetype = line[0:2]
            line = line[3:]
            kw = line[0:line.find(':')]
            line = line[(line.find(':') + 1):(len(line) - 1)]
            wordlist = line.split(',')

            for word in wordlist:
                self.__components[word] = SQLComponent(nodetype, kw)

        f.close()

    @property
    def get_components(self):
        return self.__components

    def getComponentoptions(self, node, schema):
        result = set()

        if node.getWord() == "ROOT":
            result.add(SQLComponent("ROOT", "ROOT"))
            return list(result)

        valueNodes = set()
        word = node.getWord().lower()

        if word in self.__components:
            result.add(self.__components[word])
            return list(result)

        for table in schema.getTablelist():
            result.add(SQLComponent("NN", table.get_tablename, word.similarity(self.__langparser(table.get_tablename))))

            for column in table.get_columnlist:
                result.add(SQLComponent("NN", table.get_tablename + "." + column.getName, word.similarity(self.__langparser(column.getName))))

                for value in column.get_samplevalues:
                    valueNodes.add(SQLComponent("VN", table.get_tablename + "." + column.getName, word.similarity(
                        self.__langparser(value))))

        for nodeInfo in valueNodes:
            result.add(nodeInfo)

        sortedResultList = sorted(result, cmp=self.reverseScoreComparator())

        if self.isclose(float(sortedResultList[0].get_similarity()), 1.0):
            sortedResultList.insert(1, SQLComponent("UNKNOWN", "meaningless", 1.0))
        else:
            sortedResultList.insert(0, SQLComponent("UNKNOWN", "meaningless", 1.0))

        return sortedResultList


    def reverseScoreComparator(self, a, b):
        if a.score < b.score:
            return 1
        elif a.score > b.score:
            return -1
        else:
            return 0


    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)