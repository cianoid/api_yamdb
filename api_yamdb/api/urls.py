from django.urls import include, path

from api.routers import CategoryRouter
from api.views import CategoryViewSet

app_name = 'api'

category_router = CategoryRouter()
category_router.register('category', CategoryViewSet)

urlpatterns = [
    path('v1/', include(category_router.urls))
]
