class BaseTelTorException(Exception):
    pass


class UnknownError(BaseTelTorException):
    pass


class AuthorizationFailedException(BaseTelTorException):
    pass


class EmptyCategoryNameError(BaseTelTorException):
    pass


class InvalidCategoryNameError(BaseTelTorException):
    pass
