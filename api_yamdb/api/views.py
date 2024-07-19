from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from api.serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer
)
from reviews.models import Category, Comments, Review, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    ordering_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = ()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = ()

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()
