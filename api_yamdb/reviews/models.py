from django.contrib.auth import get_user_model
from django.db import models

from core.constants import CHOICES_SCORE

User = get_user_model()


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    description = models.TextField(null=True, default=None, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    score = models.IntegerField(choices=CHOICES_SCORE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    id = models.AutoField(primary_key=True)
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
