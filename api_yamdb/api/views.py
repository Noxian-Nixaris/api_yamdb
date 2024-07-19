from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import CategorySerializer, TitleSerializer
from api_yamdb.permissions import IsAdminOrReadOnly
from api.pagination import CategoryPagination
from reviews.models import Category, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    ordering_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoryPagination
