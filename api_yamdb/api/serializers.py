import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.constants import (
    CHOICES_SCORE, MAX_SCORE, MIN_SCORE, NAME_MAX_LENGTH, SLUG_MAX_LENGTH
)
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
    # genre = GenreSerializer(source='genre_title__genre__slug', many=True)
    genre = GenreTitleSerializer(source='genre_title', many=True)
    rating = serializers.FloatField(read_only=True)

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
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.ChoiceField(choices=CHOICES_SCORE)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if not isinstance(value, int) or not (MIN_SCORE <= value <= MAX_SCORE):
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        existing_review = Review.objects.filter(
            author=author,
            title_id=title_id
        )
        if request.method == 'PATCH':
            return data
        if existing_review.exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )
        return data


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
