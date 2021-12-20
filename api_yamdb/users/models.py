from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    USER_ROLES = [
        ('Admin', 'Администратор'),
        ('Moderator', 'Модератор'),
        ('User', 'Пользователь'),
    ]

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
        default='User'
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
