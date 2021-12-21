from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Review, Title

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnlyPermission, AuthorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)


class CategoryAndGenreViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                              mixins.ListModelMixin, mixins.DestroyModelMixin):
    lookup_field = 'slug'
    lookup_value_regex = '[-a-zA-Z0-9_]+'

    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


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
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly, ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title,
                                  pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.review.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly, ]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()
