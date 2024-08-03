from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    MAX_LENGTH, EMAIL_MAX_LENGTH, CONFIRMATION_CODE_MAX_LENGTH,
    ROLE_MAX_LENGTH, PATTERN_VALIDATOR, username_not_me_validator,
    ROLE_USER, ROLE_MODERATOR, ROLE_ADMIN
)


class User(AbstractUser):

    ROLE_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_MODERATOR, 'Moderator'),
        (ROLE_ADMIN, 'Admin'),
    )
    username = models.CharField(
        max_length=MAX_LENGTH,
        validators=[PATTERN_VALIDATOR, username_not_me_validator],
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        verbose_name='Почта'
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH,
        blank=True,
        verbose_name='Код подтверждения'
    )
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        blank=True,
        verbose_name='Роль',
        default=ROLE_USER
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография')

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
