from Model.NLHandler import Node
from Model.NLHandler import Parser

class ParseTree:
    mod = None
    root = None
    nodelist = list()
    indexOfRightCoreNode = -1
    indexOfLeftCoreNode = -1

    def __init__(self, question=None, parser=None):
        self.indexOfRightCoreNode = -1
        self.indexOfLeftCoreNode = -1




