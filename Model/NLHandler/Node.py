class Node:
    """
        A class used to represent a node of a Parsetree

        Attributes
        ----------
        word : Word
            the token
        component : SQLComponent
            the sql component of the node
        parent : Node
            the parent of the node
        children : Node[]
            the list of the children of the node

        Methods
        -------
        addChild(node):
            Adding new child to the children list
        """

    def __init__(self, word=None, component=None):
        self.__word = word
        self.__component = component
        self.__parent = None
        self.__children = []

    @property
    def getIndex(self):
        return self.__index

    @property
    def getWord(self):
        return self.__word

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

    def setParent(self, node):
        self.__parent = node

    @property
    def getChildren(self):
        return self.__children

    def setChildren(self, nodelist):
        self.__children = nodelist

    def addChild(self, node):
        self.__children.append(node)
