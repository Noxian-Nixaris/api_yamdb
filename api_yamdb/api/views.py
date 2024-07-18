from rest_framework import filters, viewsets

from api.serializers import TitleSerializer
from reviews.models import Category, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    ordering_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
