import spacy
from Model.NLHandler import ParseTree
from spacy import displacy

#class Parser:
nlp = spacy.load('en_core_web_lg')
userquestion = nlp('Spacy is my tool, and I am trying to use it.')

#for sentence in userquestion.sents:
#    print(sentence)

tokens = [[token.text, token.pos_, token.tag_, token.dep_, token.head.text, token.lemma_] for token in userquestion]



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




