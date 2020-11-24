class SQLComponent:
    def __init__(self, type: str, component: str, similarity = 1.0):
        self.__type = type
        self.__component = component
        self.__similarity = similarity

    @property
    def get_type(self):
        return self.__type

    @property
    def get_component(self):
        return self.__component

    @property
    def get_similarity(self):
        return self.__similarity

    def setSimilarity(self, value):
        self.__similarity = value

