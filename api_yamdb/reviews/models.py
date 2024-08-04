from django.contrib.auth import get_user_model
from django.db import models

from core.constants import CHOICES_SCORE, DISPLAY_LENGTH, NAME_MAX_LENGTH

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:DISPLAY_LENGTH]


class Genre(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    year = models.SmallIntegerField()
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    description = models.TextField(null=True, default=None, blank=True)
    genre = models.ManyToManyField(to=Genre, through=GenreTitle)

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=CHOICES_SCORE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

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
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text
