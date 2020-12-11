from Model.NLHandler.ParseTree import ParseTree
from Model.NLHandler.Parser import Parser
from Model.NLHandler.Translator import Translator
from Model.DBHandler.Schema import Schema
from Model.DBHandler.Query import Query
from Model.DBHandler.Connection import Connection

class ProgControl:
    def __init__(self):
        self.connection = Connection()
        self.schema = None
        self.parser = None
        self.schema = None
        self.query = None
        self.host = ""
        self.dbname = ""
        self.user = ""
        self.password = ""
        self.nodelist = []
        self.choiceslist = []
        self.pt = None

    # todo
    def initDBConnention(self):
        if self.connection.connect(self.host, self.dbname, self.user, self.password):
            self.schema = Schema(self.connection.connection, self.dbname)
            self.parser = Parser(self.schema)
            return True
        else:
            return False


    def processQuestion(self, input):
        self.pt = self.parser.createParsetree(input)
        return self.mappingNodes()

    def mappingNodes(self):
        for node in self.pt.get_nodelist:
            self.nodelist.append(node)
            self.choiceslist.append(self.parser.getComponentoptions(node)[:5])

        return True

    def setChoices(self, choicelist):
        for i in range(len(choicelist)):
            self.pt.get_nodelist[i].setComponent(self.choiceslist[i][choicelist[i]])
        self.pt.removeunknownnodes()
        self.translatePt()


    def translatePt(self):
        translator = Translator(self.pt, self.schema)
        self.query = translator.translateParsetree()






