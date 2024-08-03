from django.db.models import Avg
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
from api.permissions import IsAdminOrReadOnly
from reviews.models import Category, Genre, Review, Title


class ListCreateDestroyViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    ordering = ('name', 'id',)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = (TitleFilter,)
    filterser_fields = ('name', 'year', 'category', 'genre_title__genre__slug')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer

    # def get_queryset(self):
    #     titles = Title.objects.all()
    #     filters = self.request.query_params
    #     if 'genre' in filters:
    #         filter_field = filters.get('genre')
    #         titles = titles.filter(
    #             genre_title__genre__slug=filter_field
    #         )
    #     if 'category' in filters:
    #         filter_field = filters.get('category')
    #         titles = titles.filter(category__slug=filter_field)
    #     if 'name' in filters:
    #         filter_field = filters.get('name')
    #         titles = titles.filter(name=filter_field)
    #     if 'year' in filters:
    #         filter_field = filters.get('year')
    #         titles = titles.filter(
    #             year=filter_field
    #         )
    #     return titles


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.get_base_queryset(Review, 'review_id', 'comments')

    def perform_create(self, serializer):
        super().perform_create(serializer, Review, 'review_id', 'review')


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
