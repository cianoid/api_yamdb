from datetime import datetime

from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        depth = 1


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, many=False, read_only=False)
    genre = GenreSerializer(required=False, many=True)
    rating = serializers.SerializerMethodField('get_rating', read_only=True)

    def get_rating(self, obj):
        rating = 0

        ratings = [review.score for review in
                   Review.objects.filter(title_id=obj.pk)]
        if ratings:
            rating = round(sum(ratings) / len(ratings))

        return rating

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя постить посты из будущего')

        return value

    class Meta:
        fields = '__all__'
        model = Title
