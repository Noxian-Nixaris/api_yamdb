from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.path.endswith('/me/') and request.method == 'GET':
            return user.is_authenticated

        if request.method == 'GET':
            return user.is_authenticated and user.role == 'admin'
        return True


class NotUserForPatch(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == 'PATCH' and user.role in ['user', 'moderator']:
            return False
        return True
