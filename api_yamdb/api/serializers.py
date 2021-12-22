from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, TitlesGenre
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializerList(serializers.ModelSerializer):
    category = CategorySerializer(required=False, many=False, read_only=True)
    genre = GenreSerializer(required=False, many=True)
    rating = serializers.SerializerMethodField('get_rating', read_only=True)

    def get_rating(self, obj):
        rating = None

        ratings = [review.score for review in
                   Review.objects.filter(title_id=obj.pk)]
        if ratings:
            rating = round(sum(ratings) / len(ratings))

        return rating

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    genre = serializers.ListField(required=False)

    def to_representation(self, instance):
        return TitleSerializerList(instance).to_representation(instance)

    def validate(self, attrs):
        fields = {
            'category': attrs.get('category'),
            'genre': attrs.get('genre')}
        errors = {}

        if (fields['category'] is not None and
                not Category.objects.filter(slug=fields['category']).exists()):
            errors.update({'category': 'Таких записей нет в БД'})

        if (fields['genre'] is not None and
                Genre.objects.filter(slug__in=fields['genre']).count() !=
                len(fields['genre'])):
            errors.update({'genre': 'Таких записей нет в БД'})

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')

        data = validated_data
        data['category'] = Category.objects.get(slug=category)

        obj = Title(**data)
        obj.save()

        for genre in genres:
            TitlesGenre(title=obj, genre=Genre.objects.get(slug=genre)).save()

        return obj

    def update(self, obj, validated_data):
        genres = None
        category = None

        if validated_data.get('genre') is not None:
            genres = validated_data.pop('genre')

        if validated_data.get('category') is not None:
            category = validated_data.pop('category')

        data = validated_data
        if category:
            data['category'] = Category.objects.get(slug=category)

        for field, value in data.items():
            if getattr(obj, field) != value:
                setattr(obj, field, value)

        obj.save()

        if genres:
            TitlesGenre.objects.filter(title=obj).delete()

            for genre in genres:
                TitlesGenre(title=obj, genre=Genre.objects.get(slug=genre)).save()

        return obj

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя постить посты из будущего')

        return value

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        ]


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.username = validated_data.get(
            'username',
            instance.username
        )
        instance.bio = validated_data.get(
            'bio',
            instance.bio
        )
        instance.email = validated_data.get(
            'email',
            instance.email
        )

        if instance.role == 'admin' or instance.is_staff:
            instance.role = validated_data.get(
                'role',
                instance.role
            )
        instance.save()
        return instance


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['email', 'username']
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user
            ).exists():
                raise ValidationError('Only one review is allowed')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
