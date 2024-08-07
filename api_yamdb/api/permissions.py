from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.constants import ROLE_ADMIN, ROLE_MODERATOR


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == ROLE_ADMIN
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == ROLE_ADMIN
        )


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == ROLE_MODERATOR
        )


class IsAuthModAdmOrReadOnly(BasePermission):
    """
    Пользовательский класс разрешения, который
     позволяет изменения автору, админу или модератору.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == ROLE_MODERATOR
            or request.user.role == ROLE_ADMIN
        )
