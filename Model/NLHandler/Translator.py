from Model.DBHandler.Query import *
from Model.NLHandler.Parser import Parser
from Model.NLHandler.ParseTree import ParseTree

class Translator:
    def __init__(self, parsetree):
        self.__parsetree = parsetree
        self.__query = Query()

    def translateParsetree(self):
        pass

    def translateSN(self, node):
        if node.getComponent.get_type != 'SN':
            return 'fail'
        self.translateNodes(node.getChildren)

    def translateNodes(self, nodelist):
        for n in nodelist:

