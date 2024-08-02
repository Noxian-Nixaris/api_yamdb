import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status

from core.constants import CHOICES_SCORE, NAME_MAX_LENGTH, SLUG_MAX_LENGTH
from reviews.models import Category, Comments, Genre, GenreTitle, Title, Review


User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category"""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreTitleSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели GenreTitle"""

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
        return {'name': str(value.genre.name), 'slug': str(value.genre.slug)}


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для отображения"""

    category = CategorySerializer()
    # genre = serializers.SlugRelatedField(
    #     slug_field='genre_title__genre__slug',
    #     allow_empty=False,
    #     queryset=Genre.objects.all(),
    #     many=True
    # )
    # genre = GenreSerializer(many=True)
    genre = GenreTitleSerializer(source='genre_title', many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            return total_score / reviews.count()
        return None

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
        fields = ('id', 'text', 'review', 'pub_date', 'author')
        model = Comments
        read_only_fields = ('review', 'pub_date', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.ChoiceField(choices=CHOICES_SCORE)

    class Meta:
        fields = ('id', 'text', 'score', 'pub_date', 'author', 'title')
        model = Review
        read_only_fields = ('pub_date', 'title', 'author')

    def validate_score(self, value):
        if not isinstance(value, int) or not (1 <= value <= 10):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Нельзя создать пустой отзыв')
        return value


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для внесения изменений"""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        allow_null=False,
        allow_empty=False,
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
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
