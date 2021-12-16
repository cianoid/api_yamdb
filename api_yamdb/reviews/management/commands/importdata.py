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
    help = 'Import test data. Before import wipes data from model table'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', type=str, help='Path to .csv file with data')
        parser.add_argument(
            'model', type=str, help='Model associated with data from filename')
        parser.add_argument(
            '--relation-field', type=str, help='Many-to-Many relation field')

    def change_keys(self, model, item):
        relation_data = {
            Title: {'category': Category},
            # @TODO waiting for merge with other branches
            # Reviews: {'author': User},
            # Comments: {'author': User},
        }

        rel_data = relation_data.get(model)

        if rel_data is None:
            return item

        for model_field, related_model in rel_data.items():
            obj = get_object_or_404(related_model, pk=item[model_field])
            item[model_field] = obj

        return item

    def handle(self, *args, **options):
        filename = options.get('filename')
        model_name = options.get('model')
        relation_field = options.get('relation_field')

        model_field_id = model_name.lower() + '_id'
        Model = apps.get_model('reviews', model_name)

        if not os.path.isfile(filename):
            self.stderr.write(f'File {filename} not found')
            raise SystemExit

        if relation_field:
            relation_field_id = relation_field + '_id'

            with open(filename, newline='') as csvfile:
                csvdata = csv.DictReader(csvfile)

                for item in csvdata:
                    obj = get_object_or_404(Model, pk=item[model_field_id])
                    getattr(obj, relation_field).add(item[relation_field_id])
                    obj.save()

            raise SystemExit

        with open(filename, newline='') as csvfile:
            csvdata = csv.DictReader(csvfile)
            for item in csvdata:
                item = self.change_keys(Model, item)
                obj = Model(**item)
                obj.save()
