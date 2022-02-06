import typing as tp

from utils.permissions import BasePermission, SAFE_METHODS


class IsAuthenticateCreateVideoPermission(BasePermission):
    """
    Permission class for creating new video if you authenticate
    """

    def has_permission(self) -> bool:
        return bool(
            self.request.method in SAFE_METHODS or self.request.user is not None
        )


class IsOwnerOrReadOnlyVideoPermission(BasePermission):
    """
    Permission for is owner if method in delete or patch or for read only
    """

    def has_object_permission(self, obj: tp.Any) -> bool:
        return bool(
            self.request.method in SAFE_METHODS or obj.account_id == self.request.user.id
        )
