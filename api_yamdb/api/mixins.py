from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .permissions import IsAuthModAdmOrReadOnly


class PermissionMixin:
    """Миксин, распределяющий права доступа, в зависимости от запроса."""

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (permissions.AllowAny(),)
        if self.action in ['partial_update', 'destroy']:
            return (
                permissions.IsAuthenticatedOrReadOnly(),
                IsAuthModAdmOrReadOnly(),
            )
        return (permissions.IsAuthenticated(),)


class BaseGetQuerysetMixin:
    """Миксин для получения queryset на основе параметров из URL."""

    def get_base_queryset(
        self, model, url_kwarg_one, related_name, url_kwarg_two=None
    ):
        obj_id = self.kwargs.get(url_kwarg_one)
        if url_kwarg_two:
            obj_two_id = self.kwargs.get(url_kwarg_two)
            obj = get_object_or_404(model, title=obj_two_id, id=obj_id)
        else:
            obj = get_object_or_404(model, id=obj_id)
        return getattr(obj, related_name).all()


class BaseCreateMixin:
    """
    Миксин, сохраняющий объект модели с указанием
     связанного объекта через URL-параметр.
    """

    def perform_create(
            self,
            serializer,
            model,
            url_kwarg_one,
            related_field,
            url_kwarg_two=None
    ):
        obj_id = self.kwargs.get(url_kwarg_one)
        if url_kwarg_two:
            obj_two_id = self.kwargs.get(url_kwarg_two)
            obj = get_object_or_404(model, title=obj_two_id, id=obj_id)
        else:
            obj = get_object_or_404(model, id=obj_id)
        serializer.save(**{related_field: obj}, author=self.request.user)
