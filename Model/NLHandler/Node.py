class Node:
    def __init__(self, type,  index=0, word=None, component=None):
        self.__index = index
        self.__word = word
        self.__type = type
        self.__component = component
        self.__parent = None
        self.__children = list()

    @property
    def getIndex(self):
        return self.__index

    @property
    def getWord(self):
        return self.__word

    @property
    def getType(self):
        return self.__type

    def getText(self):
        return self.__word.get_text()

    @property
    def getComponent(self):
        return self.__component

    def setComponent(self, component):
        self.__component = component

    @property
    def getParent(self):
        return self.__parent

    @property
    def getChildren(self):
        return self.__children


