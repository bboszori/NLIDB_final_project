import spacy
from Model.NLHandler import ParseTree
from Model.NLHandler import Node
from Model.NLHandler import Word
from spacy import displacy

class Parser:
    nlp = spacy.load('en_core_web_sm')

    def __init__(self):
        pass


    def createParsTree(self, text):
        userquestion = self.nlp(text)
        pt = ParseTree()
        root = Node()
        ctoken = [s for s in userquestion.sents][0].root
        w = Word(ctoken.text, ctoken.pos_, ctoken.tag_, ctoken.lemma_, ctoken.dep_)
        for i in userquestion.ents:
            if ctoken == i:
                w.ent = i.label_
        n = Node(w)
        n.parent = root
        root.children.add(n)
        pt.nodelist.add(root)
        pt.nodelist.add(n)
        children_list = [token for token in ctoken.children]

        for token in children_list:
            w = Word(token.text, token.pos_, token.tag_, token.lemma_, token.dep_)
            for i in userquestion.ents:
                if token == i:
                    w.ent = i.label_
            n = Node(w)
            pt.nodelist.add(n)






#for sentence in userquestion.sents:
#    print(sentence)

tokens = [[token.text, token.pos_, token.tag_, token.dep_, token.head.text, token.lemma_] for token in userquestion]
for i in tokens:
     print(i)

sentence = [s for s in userquestion.sents][0]
print(sentence.root)

displacy.serve(userquestion, style='dep')



# for word  in userquestion:
#     #print(word.text, word.shape_, word.is_alpha, word.is_stop)
#     print(word.text, word.pos_, word.tag_, word.dep_, word.lemma_)
#
# for word  in userquestion.ents:
#     print(word.text, word.label_)

#print(spacy.explain('VBG'))
#rint(displacy.render(userquestion, style='dep'))

# for token in userquestion.noun_chunks:
#     print(token.root.text, token.root.head.text)

# class Parser:
#     nlp = spacy.load('en_core_web_lg')
#     userquestion = None
#
#     def __init__(self, text=None):
#         if text == None:
#             pass
#         else:
#             self.userquestion = nlp(text)




