import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status

from core.constants import CHOICES_SCORE, NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Comments, Genre, GenreTitle, Title, Review


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


class GenreTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.all()
    )

    class Meta:
        model = GenreTitle
        fields = ('title', 'genre')

    def to_representation(self, value):
        return str(value.genre.slug)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreTitleSerializer(source='genre_title', many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            return total_score / reviews.count()
        return 0

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'category', 'genre', 'rating'
        )


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


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre', 'rating')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError()
        return value

    def validate_category(self, value):
        categories = Category.objects.all()
        if value not in categories:
            raise serializers.ValidationError()
        return value

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres_data:
            if Genre.objects.filter(name=genre).exists:
                GenreTitle.objects.create(title=title, genre=genre)
        return title

    def to_representation(self, instance):
        return TitleSerializer(instance=instance).data
