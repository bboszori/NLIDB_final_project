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

    def __init__(self, index, word, posTag, component=None):
        self.index = index
        self.word = word
        self.posTag = posTag
        self.component = component
        self.parent = None
        self.children = list()

