# api/admin.py
from django.contrib import admin
from .models import Client, Project

# Simple registration
admin.site.register(Client)
admin.site.register(Project)