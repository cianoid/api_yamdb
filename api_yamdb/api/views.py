import uuid

from django.core.mail import send_mail
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.filters import TitleFilter
from api.permissions import AdminOrReadOnlyPermission
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, SignUpSerializer)
from reviews.models import Category, Genre, Title
from users.models import User


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

class UserViewSet(viewsets.ModelViewSet):
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code_and_create_user(self, request):
    """Создаёт пользователя 
    и отправляет код подтверждения при регистрации.
    """
    email = request.data.get('email')
    if User.objects.filter(email=email).exists():
        message = 'Пользователь с таким email уже существует'
        return Response(
            message, status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = str(uuid.uuid4()) # uuid4 - Generate a random UUID
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid:
        User.objects.create_user(
            request.data['email'],
            username=request.data.get('username'),
            password='',
            confirmation_code=confirmation_code
        )
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {confirmation_code}',
            'info@yamdb.ru',
            [email,],
        )
        return Response(
            'Код подтверждения отправлен на указанный email',
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)