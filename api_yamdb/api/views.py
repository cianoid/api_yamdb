from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnlyPermission
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


class CategoryAndGenreViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                              mixins.ListModelMixin, mixins.DestroyModelMixin):
    lookup_field = 'slug'
    lookup_value_regex = '[-a-zA-Z0-9_]+'

    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class CategoryViewSet(CategoryAndGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')
