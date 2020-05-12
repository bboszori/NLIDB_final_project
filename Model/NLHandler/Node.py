# Az elemző fa nod-ja
from Model.NLHandler import SQLComponent

class Node:
    index = 0
    # NL szó
    word = None

    #A word-höz tartozó Part of Speech tag
    posTag = None

    #az elemző fában az adott node-hoz kapcsolódó szülő és gyermek node-ok
    parent = None
    children = list()

    #SQL component
    component = None

    def __init__(self, index=0, word=None, component=None):
        self.index = index
        self.word = word
        self.component = component
        self.parent = None
        self.children = list()

    def removeChild(self, child):
        self.children = [childeNode for childeNode in self.children if childeNode != child]
        return

    def printNodeArray(self):
        nodes = self.genNodesArray(self)
        for node in nodes:
            print("type: " + node.getInfo().getType() + " value: " + nodes.getInfo().getValue())

    def genNodesArray(self):
        nodesList = list()
        stack = list()
        stack.insert(0, self)

        while len(stack) != 0:
            curr = stack.pop(-len(stack))
            nodesList.append(curr)
            currChildren = curr.getChildren()
            for i in range(len(currChildren) - 1, -1, -1):
                stack.insert(0, currChildren[i])

        nodes = list()
        for node in nodesList:
            nodes.append(node)

        return nodes

    def equals(self, obj):
        if obj is None:
            return False
        if not (self.__class__ == obj.__class__):
            return False

        other = obj
        if not self.index == other.index:
            return False

        if not self.word == other.word:
            return False

        if not self.posTag == other.posTag:
            return False

        if self.children != other.children:
            if (self.children is None) or (other.children is None):
                return False
            if len(self.children) != len(other.children):
                return False

            if not self.isEqualsNodeList(self.children, other.children):
                return False
        return True

    def isEqualsNodeList(self, list1, list2):
        for node1 in list1:
            if node1 not in list2:
                return False
        return True