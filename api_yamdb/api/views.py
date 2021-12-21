from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from api.filters import TitleFilter
from api.permissions import AdminOrReadOnlyPermission, AdminOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, SignUpSerializer,
                             UserSerializer)
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly]


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code_and_create_user(request):
    """Создаёт пользователя
    и отправляет код подтверждения при регистрации.
    """
    email = request.data.get('email')
    username = request.data.get('username')
    if username == 'me':
        return Response(
            'Использование такого имени запрещено',
            status=status.HTTP_400_BAD_REQUEST
        )
    if User.objects.filter(email=email).exists():
        return Response(
            'Пользователь с таким email уже существует',
            status=status.HTTP_400_BAD_REQUEST
        )
    if User.objects.filter(username=username).exists():
        return Response(
            'Пользователь с таким username уже существует',
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=username, email=email, password=None
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Код подтверждения: {confirmation_code}',
            'info@yamdb.ru',
            [email, ],
        )
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tokens(user):
    """Создаёт токен в нужном формате"""
    tokens = RefreshToken.for_user(user)

    return {
        'access': str(tokens.access_token)
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt(request):
    """Выдаёт JW-токен"""
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(
        user, confirmation_code
    ):
        return Response(
            'Некорректный код подтверждения',
            status=status.HTTP_400_BAD_REQUEST
        )
    response = get_tokens(user)
    return Response(response, status=status.HTTP_200_OK)
