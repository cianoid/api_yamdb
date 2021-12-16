import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    USER_ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]
    # email и username есть в модели, но нужна уникальность
    email = models.EmailField(
        'Адрес электронной почты',
        blank=True,
        unique=True
    )
    username = models.CharField(
        'Имя',
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=USER_ROLES,
        default='user'
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True,
        default=uuid.uuid4  # uuid4 - Generate a random UUID
    )
