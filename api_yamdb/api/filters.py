from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    year = filters.DateTimeFilter(field_name='year', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')

    # def filter(self, queryset, value):
    #     print('************************************', value)
    #     if 'genre' in value:
    #         filter_field = queryset.get('genre')
    #         queryset = queryset.filter(
    #             genre_title__genre__slug=filter_field
    #         )
    #     if 'category' in value:
    #         filter_field = value.get('category')
    #         queryset = queryset.filter(category__slug=filter_field)
    #     if 'name' in value:
    #         filter_field = value.get('name')
    #         queryset = queryset.filter(name=filter_field)
    #     if 'year' in value:
    #         filter_field = value.get('year')
    #         queryset = queryset.filter(
    #             year=filter_field
    #         )
    #     return queryset
