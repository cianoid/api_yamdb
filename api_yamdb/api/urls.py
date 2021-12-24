from django.urls import include, path
from rest_framework import routers

from api.routers import CategoryAndGenreRouter
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, get_jwt,
                       send_code_and_create_user)

app_name = 'api'

category_and_genre_router = CategoryAndGenreRouter()
category_and_genre_router.register(
    'categories', CategoryViewSet, basename='categories')
category_and_genre_router.register('genres', GenreViewSet, basename='genres')

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

router.registry.extend(category_and_genre_router.registry)

auth_patterns = [
    path('signup/', send_code_and_create_user, name='send_confirmation_code'),
    path('token/', get_jwt, name='get_token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),
]
