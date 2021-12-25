from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ADMIN_NAME = 'Администратор'
    MODERATOR_NAME = 'Модератор'
    USER_NAME = 'Пользователь'


class User(AbstractUser):
    """Модель пользователя"""
    ROLE_CHOICES = [
        (UserRoles.ADMIN, UserRoles.ADMIN_NAME),
        (UserRoles.MODERATOR, UserRoles.MODERATOR_NAME),
        (UserRoles.USER, UserRoles.USER_NAME)
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=UserRoles.USER
    )
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        """Проверяет наличие роли Модератор."""
        return self.role == UserRoles.MODERATOR

    @property
    def is_admin(self):
        """Проверяет аличие роли Администратор."""
        return self.role == UserRoles.ADMIN
