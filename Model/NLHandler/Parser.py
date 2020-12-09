import spacy
from queue import Queue
from Model.NLHandler.ParseTree import ParseTree
from Model.NLHandler.Node import Node
from Model.NLHandler.Word import Word
from Model.DBHandler.Schema import Schema
from Model.NLHandler.SQLComponent import SQLComponent
from operator import attrgetter
import string
import re
from collections import Counter
from math import sqrt

class Parser:
    def __init__(self, schema):
        self.nlp = spacy.load('en_core_web_sm')
        self.__schema = schema
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

        text = question
        #text = text.translate(str.maketrans('', '', string.punctuation))
        #text = " ".join(re.split("\s+", text, flags=re.UNICODE))
        userquestion = self.nlp(text)

        sentence = list(userquestion.sents)
        root = sentence[0].root
        rootnode = Node(word=Word(root))
        ptroot = Node(word="ROOT")
        pt.set_root(ptroot)
        rootnode.setParent(ptroot)
        ptroot.addChild(rootnode)
        pt.addnode(rootnode)

        children = Queue()

        for child in root.children:
            n = Node(word=Word(child))
            n.setParent(rootnode)
            rootnode.addChild(n)
            pt.addnode(n)
            children.put(child)

        while not children.empty():
            currchild = children.get()
            currnode = pt.findNodebyToken(currchild)
            for child in currchild.children:
                n = Node(word=Word(child))
                n.setParent(currnode)
                currnode.addChild(n)
                pt.addnode(n)
                children.put(child)

        return pt

    def word2vec(self, txt):
        # count the characters in word
        cw = Counter(txt)
        # precomputes a set of the different characters
        sw = set(cw)
        # precomputes the "length" of the word vector
        lw = sqrt(sum(c * c for c in cw.values()))
        # return a tuple
        return cw, sw, lw

    def cosdis(self, v1, v2):
        # which characters are common to the two words?
        common = v1[1].intersection(v2[1])
        # by definition of cosine distance we have
        return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]

    def similarityText(self, text1, text2):
        v1 = self.word2vec(text1)
        v2 = self.word2vec(text2)
        return self.cosdis(v1, v2)

    def getComponentoptions(self, node):
        result = set()

        # if node.getWord() == "ROOT":
        #     result.add(SQLComponent("ROOT", "ROOT"))
        #     return list(result)

        valueNodes = set()
        word = node.getWord.get_text().lower()

        if word in self.__components:
            result.add(self.__components[word])
            #return list(result)

        for table in self.__schema.getTablelist():
            result.add(SQLComponent("NN", table.get_tablename, self.similarityText(word, table.get_tablename.lower())))

            for column in table.get_columnlist:
                result.add(SQLComponent("NN", table.get_tablename + "." + column.getName, self.similarityText(word,
                                                                                                            column.getName.lower())))

                for value in column.get_samplevalues:
                    if value[0] != None:
                        valueNodes.add(SQLComponent("VN", table.get_tablename + "." + column.getName, self.similarityText(
                            word, str(value[0]).lower())))

        for nodeInfo in valueNodes:
            result.add(nodeInfo)

        sortedResultList = sorted(result, key=attrgetter('similarity'), reverse=True)

        if sortedResultList[0].get_similarity < 0.75:
            sortedResultList.insert(0, SQLComponent("UNKNOWN", "UNKNOWN", 1.0))

        return sortedResultList









