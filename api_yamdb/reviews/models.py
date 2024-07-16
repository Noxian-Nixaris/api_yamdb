from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories'
        )


class Review(models.Model):
    text = models.TextField()
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'reviews'


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)


class Comments(models.Model):
    text = models.TextField()
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'comments'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)

    class Meta:
        default_related_name = 'genre_title'
