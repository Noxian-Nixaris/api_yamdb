from django.shortcuts import get_object_or_404
from rest_framework import filters, response, status, viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer
)
from api_yamdb.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.pagination import CategoryPagination
from reviews.models import Category, Comments, Genre, Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    ordering_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    ordering = ('name', 'id',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    ordering = ('name', 'id',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # def destroy(self, request, *args, **kwargs):
    #     obj = get_object_or_404(self.get_queryset(), slug=self.kwargs['slug'])
    #     self.perform_destroy(obj)
    #     return response.Response(status=status.HTTP_204_NO_CONTENT)
