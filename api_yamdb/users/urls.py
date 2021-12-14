from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, SignUpViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/signup/',
        SignUpViewSet,
        name='sign_up'
    )
]
