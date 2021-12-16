from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports test data'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='Path to .csv file with data')
        parser.add_argument(
            'model', type=str, help='Model associated with data from filename')

    def handle(self, *args, **options):
        filename = options.get('filename')
        model_name = options.get('model')

