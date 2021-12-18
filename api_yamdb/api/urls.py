from django.urls import include, path

from rest_framework import routers

from api.routers import CategoryAndGenreRouter
from api.views import CategoryViewSet

app_name = 'api'

category_and_genre_router = CategoryAndGenreRouter()
category_and_genre_router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(category_and_genre_router.urls)),
    path('v1/', include('users.urls')),
]
