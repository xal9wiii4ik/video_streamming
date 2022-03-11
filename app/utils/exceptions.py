import typing as tp


class BaseErrorException(Exception):
    """
    Base exception class for handler exceptions
    """

    def __init__(self, message: tp.Union[str, tp.Dict[str, str]]) -> None:
        self.message = message


class LimitOffsetError(BaseErrorException):
    """
    Exception class for limit and offset
    """

    pass


class SortException(BaseErrorException):
    """
    Exception class sort and sort_type
    """

    pass


class EmptyBodyException(BaseErrorException):
    """
    Exception for empty body if this create or update
    """

    pass


class SerializerValidationError(BaseErrorException):
    """
    Exception for serializer
    """

    pass
