from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, permissions, exceptions
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleCreateUpdateSerializer
)
from api_yamdb.permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrReadOnly,
    IsAuthModAdmOrReadOnly
)
from api.pagination import CategoryPagination
from reviews.models import Category, Comments, Genre, Review, Title


class ListCreateDestroyViewSet(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями"""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    ordering_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    ordering = ('name', 'id',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для работы с категориями"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    ordering = ('name', 'id',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['partial_update', 'destroy']:
            return [IsAuthModAdmOrReadOnly()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        try:
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:
            raise exceptions.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями"""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAdminOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для работы с жанрами"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
