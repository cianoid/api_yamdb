from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from api.filters import TitleFilter
from api.permissions import (AdminOrReadOnlyPermission, AdminOrSuperuser,
                             AuthorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, SignUpSerializer,
                             ConfirmationCodeSerializer, UserSerializer,
                             UserMeSerializer)
from reviews.models import Category, Genre, Title, Review
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
    """Вьюсет для модели User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminOrSuperuser]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code_and_create_user(request):
    """Создаёт пользователя и отправляет код подтверждения"""
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


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt(request):
    """Выдаёт JW-токен"""
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(
        user, confirmation_code
    ):
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


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
