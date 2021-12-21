from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
