from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    confirmation_code = models.CharField(max_length=6, blank=True)
    role = models.CharField(max_length=26, choices=ROLES, default='user')
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['username']
