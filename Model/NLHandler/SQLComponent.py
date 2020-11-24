class SQLComponent:
    def __init__(self, type, component):
        self.__type = type
        self.__component = component

    @property
    def get_type(self):
        return self.__type

    @property
    def get_component(self):
        return self.__component

