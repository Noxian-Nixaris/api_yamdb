from rest_framework.permissions import BasePermission

from core.constants import ROLE_ADMIN


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.role == ROLE_ADMIN
            or user.is_superuser
        )
