from django.contrib.auth import get_user_model
from django.db import models

from core.constants import (
    CHOICES_SCORE, DISPLAY_LENGTH, NAME_MAX_LENGTH
)
from core.validators import year_check

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Имя')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name[:DISPLAY_LENGTH]


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Имя')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name[:DISPLAY_LENGTH]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'genre'), name='unique_genre_title'
            )
        ]
        default_related_name = 'genre_title'


class Title(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Имя')
    year = models.SmallIntegerField(
        validators=[year_check], verbose_name='Год'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )
    description = models.TextField(
        null=True, default=None, blank=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        to=Genre, through=GenreTitle, verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'
        ordering = ('name', 'id')

    def __str__(self):
        return self.name[:DISPLAY_LENGTH]


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        choices=CHOICES_SCORE, verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        ordering = ('pub_date', 'id')
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('pub_date', 'id')

    def __str__(self):
        return self.text
