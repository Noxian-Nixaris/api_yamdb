import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status

from core.constants import NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Comments, Title, Review


User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    genre = 1

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError()
        return value

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value) > NAME_MAX_LENGTH:
            raise serializers.ValidationError(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return value

    def validate_slug(self, value):
        if len(value) > SLUG_MAX_LENGTH and value == r'^[-a-zA-Z0-9_]+$':
            raise serializers.ValidationError(
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('text', 'review', 'pub_date', 'author')
        model = Comments
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('text', 'title', 'score', 'pub_date', 'author')
        model = Review
