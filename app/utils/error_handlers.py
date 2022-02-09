import typing as tp

from flask import Response, jsonify
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError

from utils.exceptions import (
    LimitOffsetError,
    SortException,
    PermissionException,
    EmptyBodyException,
    SerializerValidationError,
)


def validation_error_handler(error: ValidationError) -> tp.Tuple[Response, int]:
    """
    Except ValidationError
    Args:
        error: current error
    Returns:
        json with status code
    """

    return jsonify(error.errors()), 400


def limit_offset_error_handler(error: LimitOffsetError) -> tp.Tuple[Response, int]:
    """
    Except LimitOffsetError
    Args:
        error: current error
    Returns:
        json with status code
    """

    return jsonify({'Error': error.message}), 400


def sort_error_handler(error: SortException) -> tp.Tuple[Response, int]:
    """
    Except LimitOffsetError
    Args:
        error: current error
    Returns:
        json with status code
    """

    return jsonify({'Error': error.message}), 400


def permission_exception_handler(error: PermissionException) -> tp.Tuple[Response, int]:
    """
    Except PermissionException
    Args:
        error: current error
    Returns:
        json with status code
    """

    return jsonify({'Error': error.message}), 401


def empty_body_exception(error: EmptyBodyException) -> tp.Tuple[Response, int]:
    """
    Except EmptyBodyException
    Args:
        error: current error
    Returns:
        json with status code
    """

    return jsonify({'Error': error.message}), 400


def serializer_validation_error(error: SerializerValidationError) -> tp.Tuple[Response, int]:
    """
    Except SerializerValidationError
    Args:
        error: current error
    Returns:
        json with status code
    """

    return jsonify(error.message), 400
