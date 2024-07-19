from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are typically read-only methods such as GET, HEAD, and OPTIONS
        if request.method in ('PATCH', 'PUT') and obj == request.user:
            return True
        return request.method in ('GET', 'HEAD', 'OPTIONS')

    def get_permissions(self, request):
        if self.action == 'delete':
            return IsAdminUser()
