from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in ['GET', 'DELETE', 'PATCH']:
            return user.is_authenticated and (user.role == 'admin'
                                              or user.is_superuser)
        return True
