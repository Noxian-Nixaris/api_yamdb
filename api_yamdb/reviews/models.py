from django.contrib.auth import get_user_model
from django.db import models

from core.constants import CHOICES_SCORE, DISPLAY_LENGTH, NAME_MAX_LENGTH

User = get_user_model()


class BaseModelClass(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:DISPLAY_LENGTH]


class ReviewCommentBaseModel(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


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

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=CHOICES_SCORE)
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


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
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
