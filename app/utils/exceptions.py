import typing as tp


class LimitOffsetError(Exception):
    """
    Exception class for limit and offset
    """

    def __init__(self, message: tp.Union[str, tp.Dict[str, str]]) -> None:
        self.message = message


class SortException(Exception):
    """
    Exception class sort and sort_type
    """

    def __init__(self, message: tp.Union[str, tp.Dict[str, str]]) -> None:
        self.message = message


class PermissionException(Exception):
    """
    Exception for permissions
    """

    def __init__(self, message: tp.Union[str, tp.Dict[str, str]]) -> None:
        self.message = message


class SerializerValidationError(Exception):
    """
    Exception for serializer
    """

    def __init__(self, message: tp.Union[str, tp.Dict[str, str]]) -> None:
        self.message = message


class EmptyBodyException(Exception):
    """
    Exception for empty body if this create or update
    """

    def __init__(self, message: tp.Union[str, tp.Dict[str, str]]) -> None:
        self.message = message
