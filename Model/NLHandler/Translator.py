from .Query import Query

class Translator:
    def __init__(self, root, schema):
        self.__schema = schema
        self.__query = Query()

        self.translateSClause(root.getChildren()[0])
            if (len(root.getChildren()) >= 2):
                self.translateComplexCondition(root.getChildren()[1])

            if schema is not None:
                self.addJoinPath()
        else:
            self.schema = schema
            self.query = SQLQuery()
            self.translateGNP(root)