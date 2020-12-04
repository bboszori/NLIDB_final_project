class SQLComponent:
    def __init__(self, type: str, component: str, similarity = 1.0, symbol=None):
        self.__type = type
        self.__component = component
        self.similarity = similarity
        self.__symbol = symbol

    @property
    def get_type(self):
        return self.__type

    @property
    def get_component(self):
        return self.__component

    @property
    def get_symbol(self):
        return self.__symbol

    @property
    def get_similarity(self):
        return self.similarity

    def setSimilarity(self, value):
        self.similarity = value

