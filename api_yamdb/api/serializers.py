from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=False)
    genre = GenreSerializer(required=True, many=True)

    class Meta:
        fields = '__all__'
        model = Title

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        ]

class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('email', 'username')
        model = User
