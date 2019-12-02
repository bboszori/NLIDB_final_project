
class Word:
    text = None
    pos = None
    tag = None
    lemma = None
    dep = None
    ent = None

    def _init_(self, text, pos, tag, lemma, dep, ent=None):
        self.text = text
        self.pos = pos
        self.tag = tag
        self.lemma = lemma
        self.dep = dep
        self.ent = ent



