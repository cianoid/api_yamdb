from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import User

try:
    admin.site.register(User)
except AlreadyRegistered:
    pass
