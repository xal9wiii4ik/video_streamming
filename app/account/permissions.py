import typing as tp

from flask import Request


def account_permission(user: tp.Any, request: Request, pk: int) -> bool:
    """
    Permission for account
    Args:
        user: current user model
        request: current request
        pk: current user pk
    Return:
        has access or no
    """

    if request.method in ['PATCH', 'DELETE']:
        return bool(pk == user.id)
    return True
