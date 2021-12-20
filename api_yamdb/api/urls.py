from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from api.routers import CategoryAndGenreRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet, SignUpView

app_name = 'api'

category_and_genre_router = CategoryAndGenreRouter()
category_and_genre_router.register('categories', CategoryViewSet)
category_and_genre_router.register('genres', GenreViewSet)

title_router = routers.DefaultRouter()
title_router.register('titles', TitleViewSet)
# Добавление роутеров категорий и жанров
title_router.registry.extend(category_and_genre_router.registry)

users_router = routers.DefaultRouter()
users_router.register('users', UserViewSet)

# зачем каждому свой дефолтный роутер? лучше так:
# router = = routers.DefaultRouter()
# router.register('titles', TitleViewSet)
# router.registry.extend(category_and_genre_router.registry)
# router.register('users', UserViewSet)

# может v1 вынести в головной  urls? 
urlpatterns = [
    # path('v1/', include(router.urls)),
    path('v1/', include(title_router.urls)),
    path('v1/', include(users_router.urls)),
    path(
        'v1/auth/signup/',
        SignUpView.as_view(),
        name='sign_up'
    ),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    )
]
