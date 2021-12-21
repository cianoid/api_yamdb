from django_filters import rest_framework as django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__slug', method='filter_by_slug')
    genre = django_filters.CharFilter(
        field_name='genre__slug', method='filter_by_slug')

    def filter_by_slug(self, queryset, field_name, value):
        return queryset.filter(**{field_name: value})

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
