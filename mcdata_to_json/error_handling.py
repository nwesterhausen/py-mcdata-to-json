class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class MissingRequiredFileError(Error):
    """Exception raised for missing a required file.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message