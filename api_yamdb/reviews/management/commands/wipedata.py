from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = 'Wipe data from tables'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Title.objects.all().delete()
        Genre.objects.all().delete()
        Category.objects.all().delete()
        Comment.objects.all().delete()
        Review.objects.all().delete()
