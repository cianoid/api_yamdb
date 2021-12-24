from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


for model in apps.get_models():
    try:
        if model.__module__ != 'reviews.models':
            raise Exception
        if not getattr(model, 'ADMIN_ZONE', True):
            raise Exception

        admin.site.register(model)
    except (AlreadyRegistered, Exception):
        pass
