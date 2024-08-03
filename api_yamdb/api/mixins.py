from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, permissions

from .permissions import IsAuthModAdmOrReadOnly


class PermissionMixin:
    """Миксин, распределяющий права доступа, в зависимости от запроса."""

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (permissions.AllowAny(),)
        if self.action in ['partial_update', 'destroy']:
            return (IsAuthModAdmOrReadOnly(),)
        return (permissions.IsAuthenticated(),)


class BaseGetQuerysetMixin:
    """Миксин для получения queryset на основе параметров из URL."""

    def get_base_queryset(self, model, url_kwarg, related_name):
        obj_id = self.kwargs.get(url_kwarg)
        obj = get_object_or_404(model, id=obj_id)
        return getattr(obj, related_name).all()


class BaseCreateMixin:
    """
    Миксин, сохраняющий объект модели с указанием
     связанного объекта через URL-параметр.
    """

    def perform_create(self, serializer, model, url_kwarg, related_field):
        obj_id = self.kwargs.get(url_kwarg)
        obj = get_object_or_404(model, id=obj_id)
        serializer.save(**{related_field: obj}, author=self.request.user)
