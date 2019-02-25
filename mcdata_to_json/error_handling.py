class Error(Exception):
    """Base class for exceptions in this module.

    Attributes:
        message -- explanation of the error"""

    def __init__(self, message):
        self.message = message


class MissingRequiredFileError(Error):
    """Exception raised for missing a required file."""
    pass


class MojangAPIError(Error):
    """Exception raised when interacting with the Mojang API"""
    pass


class Non200ResponseError(MojangAPIError):
    """Exception raised when receiving a non-OK (2xx) response"""
    pass


class InvalidQueryError(MojangAPIError):
    """Exception raised when the Mojang API returns an error

    This can happen if you are rate-limited as well."""
    pass