from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter

from reviews.models import Genre, Title


class TitleFilter(FilterSet):
    # genre = ModelMultipleChoiceFilter(
    #     field_name='genre_title__genre__slug',
    #     to_field_name='slug',
    #     queryset=Genre.objects.all()
    # )
    genre = CharFilter(field_name='genre_title__genre__slug', lookup_expr='iexact')

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
