import spacy
from queue import Queue
from Model.NLHandler.ParseTree import ParseTree
from Model.NLHandler.Node import Node
from Model.NLHandler.Word import Word

from spacy import displacy

class Parser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

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

    def similarityToken(self, t1, t2):
        return t1.similarity(t2)






