from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z',
                                   message='Имя пользователя недопустимо')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(
        max_length=6,
        blank=True
    )
    role = models.CharField(
        max_length=26,
        choices=(
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ),
        default='user'
    )
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(default=True)
