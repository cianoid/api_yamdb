from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['pk']

    @property
    def is_moderator(self):
        """Проверяет наличие роли Модератор."""
        return self.role == 'moderator'

    @property
    def is_admin(self):
        """Проверяет аличие роли Администратор."""
        return self.role == 'admin'
