import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import relations, serializers
from rest_framework import status

from core.constants import CHOICES_SCORE, NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Comments, Genre, GenreTitle, Title, Review

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log', mode='w'),
        logging.StreamHandler()
    ]
)


User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GenreTitleSerializer(serializers.ModelSerializer):
    genre_id = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    title_id = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all()
    )

    class Meta:
        model = GenreTitle
        fields = ('title_id', 'genre_id')
    
    def to_representation(self, value):
        return str(value.genre_id.slug)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    genre = GenreTitleSerializer(source='genre_id', many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            return total_score / reviews.count()
        return 0

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError()
        logging.debug(F'{value}')
        return value

    def validate_category(self, value):
        categories = Category.objects.all()
        if value not in categories:
            raise serializers.ValidationError()
        return value
    
    def to_representation(self, value):
        return str(value.genre_id.slug)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre', 'rating')


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
    score = serializers.ChoiceField(choices=CHOICES_SCORE)

    class Meta:
        fields = ('text', 'score', 'pub_date', 'author')
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message="Вы уже оставили отзыв для этого тайтла"
            )
        ]
