from django.urls import include, path
from rest_framework import routers

from api.routers import CategoryAndGenreRouter
from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       send_code_and_create_user, get_jwt)
app_name = 'api'

category_and_genre_router = CategoryAndGenreRouter()
category_and_genre_router.register('categories', CategoryViewSet)
category_and_genre_router.register('genres', GenreViewSet)

title_router = routers.DefaultRouter()
title_router.register('titles', TitleViewSet)
title_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
title_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
# Добавление роутеров категорий и жанров
title_router.registry.extend(category_and_genre_router.registry)

users_router = routers.DefaultRouter()
users_router.register('users', UserViewSet, basename='users')
users_router.register(r'users/(?P<username>[\w.@+-]+)/', UserViewSet, basename='user')

# зачем каждому свой дефолтный роутер? лучше так:
# v1_router = = routers.DefaultRouter()
# v1_router.register('titles', TitleViewSet)
# v1_router.registry.extend(category_and_genre_router.registry)
# v1_router.register('users', UserViewSet)

auth_patterns = [
    path('signup/', send_code_and_create_user, name='send_confirmation_code'),
    path('token/', get_jwt, name='get_token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    # path('v1/', include(v1_router.urls)),
    path('v1/', include(title_router.urls)),
    path('v1/', include(users_router.urls)),
]
