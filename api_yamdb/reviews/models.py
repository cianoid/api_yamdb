from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256)
    slug = models.SlugField(
        max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, default=0, on_delete=models.SET_DEFAULT,
        related_name='titles')
    genre = models.ManyToManyField(
        Genre, related_name='titles')

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField(blank=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    pub_date = models.DateTimeField(
        'review date', auto_now_add=True
    )
    score = models.IntegerField(
        'review score',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['-pub_date', ]
        unique_together = ['author', 'title']


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('comment text', blank=False)
    created = models.DateTimeField(
        'comment date', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
