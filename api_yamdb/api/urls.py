from django.urls import include, path

from rest_framework import routers

from api.routers import CategoryAndGenreRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

category_and_genre_router = CategoryAndGenreRouter()
category_and_genre_router.register('categories', CategoryViewSet)
category_and_genre_router.register('genres', GenreViewSet)

title_router = routers.DefaultRouter()
title_router.register('titles', TitleViewSet)
# Добавление роутеров категорий и жанров
title_router.registry.extend(category_and_genre_router.registry)

urlpatterns = [
    path('v1/', include(title_router.urls)),
    path('v1/', include('users.urls')),
]
