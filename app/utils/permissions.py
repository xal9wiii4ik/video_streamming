import typing as tp

from werkzeug.local import LocalProxy
from utils.exceptions import PermissionException


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class BasePermission:
    """
    A base class from which all permission classes should inherit.
    """

    def __init__(self, request: tp.Any) -> None:
        self.request = request

    def has_permission(self) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return True

    def has_object_permission(self, obj: tp.Any) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return True


class IsAuthenticate(BasePermission):
    """
    Is Authenticate permission
    """

    def has_permission(self) -> bool:
        if self.request.user is None:
            raise PermissionException('Login is required')
        return True
