from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from api.mixins import BaseCreateMixin, BaseGetQuerysetMixin, PermissionMixin
from api.pagination import CategoryPagination
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateUpdateSerializer,
    TitleSerializer
)
from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsAuthModAdmOrReadOnly
from reviews.models import Category, Genre, Review, Title


class ListCreateDestroyViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    ordering = ('name', 'id',)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = TitleFilter
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering = ('name', 'id',)
    lookup_field = 'slug'


class ReviewViewSet(
    BaseGetQuerysetMixin,
    PermissionMixin,
    BaseCreateMixin,
    viewsets.ModelViewSet
):
    """Вьюсет для работы с отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.get_base_queryset(Title, 'title_id', 'reviews')

    def perform_create(self, serializer):
        super().perform_create(serializer, Title, 'title_id', 'title')


class CommentViewSet(
    BaseGetQuerysetMixin,
    PermissionMixin,
    BaseCreateMixin,
    viewsets.ModelViewSet
):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.get_base_queryset(
            Review, 'review_id', 'comments', url_kwarg_two='title_id'
        )

    def perform_create(self, serializer):
        super().perform_create(
            serializer, Review, 'review_id', 'review', url_kwarg_two='title_id'
        )


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
