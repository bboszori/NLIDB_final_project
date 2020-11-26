
class Word:

    def _init_(self, token):
        self.__token = token

    @property
    def get_token(self):
        return self.__token

    def get_text(self):
        return self.__token.text

    def get_pos(self):
        return self.__token.pos_

    def get_tag(self):
        return self.__token.tag_

    def get_lemma(self):
        return self.__token.lemma_

    




