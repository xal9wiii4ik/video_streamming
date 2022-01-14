import typing as tp

from flask import Request


def account_permission(request: tp.Any, pk: tp.Optional[int] = None) -> bool:
    """
    Permission for account
    Args:
        request: current request
        pk: current user pk if needed
    Return:
        has access or no
    """

    if request.method in ['PATCH', 'DELETE']:
        return bool(pk == request.user.id)
    return True
