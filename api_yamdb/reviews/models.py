from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(datetime.now().year),))
    category = models.ForeignKey(
        Category, default=0, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='titles')
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True, through='TitlesGenre')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class TitlesGenre(models.Model):
    ADMIN_ZONE = False

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'review date', auto_now_add=True
    )
    score = models.IntegerField(
        'review score',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'ревью'
        verbose_name_plural = 'ревью'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique review')
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('comment text', blank=False)
    pub_date = models.DateTimeField(
        'comment date', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
