from Model.NLHandler.Node import Node
from queue import Queue

class ParseTree:
    def __init__(self):
        self.__root = None
        self.__nodelist = []


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

                for ch in node.getChildren:
                    node.getParent.addChild(ch)
                    ch.setParent(node.getParent)

