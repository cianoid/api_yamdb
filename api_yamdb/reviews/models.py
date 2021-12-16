from django.db import models


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
