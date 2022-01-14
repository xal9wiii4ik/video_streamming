import typing as tp

from flask import Request


def is_owner(request: tp.Any, pk: tp.Optional[int] = None) -> bool:
    """
    Permission for is owner
    Args:
        request: current request
        pk: current user pk if needed
    Return:
        has access or no
    """

    if request.method in ['PATCH', 'DELETE']:
        return bool(pk == request.user.id)
    return True
