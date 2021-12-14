from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = [
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
]


class User(AbstractUser):
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
