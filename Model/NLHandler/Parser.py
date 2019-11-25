import spacy
from spacy import displacy

#class Parser:
nlp = spacy.load('en_core_web_lg')
userquestion = nlp('Spacy is my tool, and I am trying to use it.')

#for sentence in userquestion.sents:
#    print(sentence)

tokens = [token.text for token in userquestion]

for word  in userquestion:
    #print(word.text, word.shape_, word.is_alpha, word.is_stop)
    print(word.text, word.pos_, word.tag_, word.dep_, word.lemma_)

for word  in userquestion.ents:
    print(word.text, word.label_)

#print(spacy.explain('VBG'))
#rint(displacy.render(userquestion, style='dep'))

for token in userquestion.noun_chunks:
    print(token.root.text, token.root.head.text)
