# Az adott node-hoz kapcsolódó SQL komponenst tartalmazza

class SQLComponent:

    type = None
    value = None
    score = 1.0

    def __init__(self, type, value, score=1.0):
        self.type = type
        self.value = value
        self.score = score #similarity

    def getType(self):
        return self.type

    def getScore(self):
        return self.score

    def getValue(self):
        return self.value

