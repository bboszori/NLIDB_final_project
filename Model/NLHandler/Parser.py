import spacy
from queue import Queue
from Model.NLHandler.ParseTree import ParseTree
from Model.NLHandler.Node import Node
from Model.NLHandler.Word import Word
from Model.DBHandler.Schema import Schema
from Model.NLHandler.SQLComponent import SQLComponent
from operator import attrgetter

from spacy import displacy

class Parser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.__components = dict()

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

    def createParsetree(self, question):
        pt = ParseTree()
        userquestion = self.nlp(question)
        sentence = list(userquestion.sents)
        root = sentence[0].root
        rootnode = Node(word=Word(root))
        l = []
        for ch in root.children:
            l.append(Node(word=Word(ch)))
        rootnode.setChildren(l)
        pt.set_root(rootnode)

        children = Queue()

        for child in root.children:
            n = Node(word=Word(child))
            n.setParent(rootnode)
            n.setChildren(list(child.children))
            pt.addnode(n)
            children.put(child)

        while not children.empty():
            currchild = children.get()
            for child in currchild.children:
                n = Node(word=Word(child))
                n.setParent(currchild)
                l = []
                for ch in child.children:
                    l.append(Node(word=Word(ch)))
                n.setChildren(l)
                pt.addnode(n)
                children.put(child)

        return pt

    def similarityText(self, text1, text2):
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        return doc1.similarity(doc2)

    def similarityToken(self, token, text):
        return token.similarity(self.nlp(text))

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
            result.add(SQLComponent("NN", table.get_tablename, self.similarityToken(word, table.get_tablename)))

            for column in table.get_columnlist:
                result.add(SQLComponent("NN", table.get_tablename + "." + column.getName, self.similarityToken(word, column.getName)))

                for value in column.get_samplevalues:
                    valueNodes.add(SQLComponent("VN", table.get_tablename + "." + column.getName, self.similarityToken(
                        word, value)))

        for nodeInfo in valueNodes:
            result.add(nodeInfo)

        sortedResultList = sorted(result, key=attrgetter('score'), reverse=True)

        return sortedResultList









