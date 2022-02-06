import typing as tp

from utils.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnlyAccountPermission(BasePermission):
    """
    Permission for account if owner or read only
    """

    def has_object_permission(self, obj: tp.Any) -> bool:
        return bool(self.request.method in SAFE_METHODS or obj.id == self.request.user.id)
