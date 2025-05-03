# api/models.py
from django.db import models
from django.contrib.auth.models import User # Use Django's built-in User

# Client Model
class Client(models.Model):
    client_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)     # Automatically set on update
    created_by = models.ForeignKey(User, related_name='created_clients', on_delete=models.CASCADE)

    def __str__(self):
        return self.client_name

# Project Model
class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name