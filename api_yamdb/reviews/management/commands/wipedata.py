import csv
import os

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

# @TODO waiting for merge with other branches
from reviews.models import Category, Genre, Title #, Comments, Reviews

User = get_user_model()


class Command(BaseCommand):
    help = 'Wipe data from tables'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Title.objects.all().delete()
        Genre.objects.all().delete()
        Category.objects.all().delete()
        # @TODO waiting for merge with other branches
        # Comments.objects.all().delete()
        # Reviews.objects.all().delete()

