from Model.NLHandler.Node import Node
from queue import Queue

class ParseTree:
    def __init__(self):
        self.__root = None
        self.__nodelist = []
        self.__indexOfRightCoreNode = -1
        self.__indexOfLeftCoreNode = -1


    @property
    def get_root(self):
        return self.__root

    def set_root(self, node):
        self.__root = node

    @property
    def get_nodelist(self):
        return self.__nodelist

    def addnode(self, node):
        self.__nodelist.append(node)

    def findNodebyToken(self, token):
        for n in self.__nodelist:
            if n.getWord.get_token == token:
                return n
        return None

    def removeunknownnodes(self):
        for node in self.__nodelist:
            if (node != self.__root) and (node.getComponent.get_type == "UNKNOWN"):
                node.getParent.getChildren.remove(node)
                node.setRemoved(True)
                print("Removing: " + node.getWord.get_text())
                for ch in node.getChildren:
                    node.getParent.addChild(ch)
                    ch.setParent(node.getParent)

    def adjustTree(self):
        self.checkSN()

    def checkSN(self):
        for n in self.__nodelist:
            if n.getComponent.get_type == 'SN':
                if n.getParent.getWord == "ROOT":
                    return
                while n.getParent.getWord != "ROOT":
                    oldparent = n.getParent
                    n.setParent(oldparent.getParent)
                    n.getParent.getChildren.remove(oldparent)
                    n.getParent.addChild(n)
                    oldparent.setParent(n)
                    oldparent.getChildren.remove(n)
                    n.addChild(oldparent)





