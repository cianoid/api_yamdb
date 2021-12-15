from rest_framework import filters, mixins, viewsets

from api.permissions import AdminOrReadOnlyPermission
from api.serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                      mixins.ListModelMixin, mixins.DestroyModelMixin):
    lookup_field = 'slug'
    lookup_value_regex = '[-a-zA-Z0-9_]+'

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
