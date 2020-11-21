class Node:
    def __init__(self, type,  index=0, word=None, component=None):
        self._index = index
        self._word = word
        self._type = type
        self._component = component
        self._parent = None
        self._children = list()

    @property
    def getIndex(self):
        return self._index

    @property
    def getWord(self):
        return self._word

    @property
    def getType(self):
        return self._type

    @property
    def getComponent(self):
        return self._component

    @property
    def getParent(self):
        return self._parent

    @property
    def getChildren(self):
        return self._children


