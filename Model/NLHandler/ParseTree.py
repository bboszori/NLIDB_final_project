from Model.NLHandler.Node import Node
from queue import Queue

class ParseTree:
    def __init__(self):
        self.__root = None
        self.__nodelist = []
        self.__indexOfRightCoreNode = -1
        self.__indexOfLeftCoreNode = -1


    @property
    def get_root(self):
        return self.__root

    def set_root(self, node):
        self.__root = node
        self.__nodelist.append(node)

    @property
    def get_nodelist(self):
        return self.__nodelist

    def addnode(self, node):
        self.__nodelist.append(node)

    def traverse(self):
        visited = []
        node_queue = Queue()
        node_queue.put(self.__root)
        for ch in self.__root.getChildren:
            node_queue.put(ch)
        while node_queue.qsize() != 0:
            next_node = node_queue.get()
            visited.append(next_node)
            ch = next_node.getChildren
            if ch != None:
                for child in ch:
                    node_queue.put(child)

        return visited
