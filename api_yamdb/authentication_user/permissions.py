from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.path.endswith('/me/') and request.method == 'GET':
            return True
        if request.method == 'GET':
            return request.user.is_superuser or request.user.role == 'admin'
        return True
