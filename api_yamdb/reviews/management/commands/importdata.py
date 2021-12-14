from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports test data'

    def handle(self, *args, **options):
        pass

