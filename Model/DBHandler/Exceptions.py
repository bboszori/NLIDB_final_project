class QueryError(Exception):
    """Exception raised for running SQL query.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="There was a problem with running the query"):
        self.message = message
        super().__init__(self.message)

class AttributeError(Exception):
    """Exception raised for not supported attribute.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="This attribute is not supported"):
        self.message = message
        super().__init__(self.message)
