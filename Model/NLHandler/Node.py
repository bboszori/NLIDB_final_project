# Az elemző fa node-ja
from Model.NLHandler import SQLComponent

class Node:
    index = 0

    word = None
    parent = None
    children = list()
    component = None

    def __init__(self, index=0, word=None, component=None):
        self.index = index
        self.word = word
        self.component = component
        self.parent = None
        self.children = list()


    def getText(self):
        return self.word.text
    def getTag(self):
        return self.word.pos
    def getChildren(self):
        return self.children
    def getComponent(self):
        return self.component

    #remove a child from the list
    def removeChild(self, child):
        self.children = [childNode for childNode in self.children if not childNode.equals(child)]
        return

    def generateNodeList(self):
        nodeList = list()
        stack = list()
        stack.insert(0, self)

        while len(stack) != 0:
            current = stack.pop(-len(stack))
            nodeList.append(current)
            currentChildren = current.getChildren()
            for i in range(len(currentChildren) - 1, -1, -1):
                stack.insert(0, currentChildren[i])

        nodes = list()
        for node in nodeList:
            nodes.append(node)

        return nodes

    def equals(self, other):
        if other is None:
            return False
        if not (self.__class__ == other.__class__):
            return False

        other = other
        if not self.index == other.index:
            return False

        if not self.getText() == other.getText():
            return False

        if not self.getTag() == other.getTag():
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