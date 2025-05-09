# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic User info"""
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project details (less verbose)"""
    created_by = serializers.StringRelatedField(read_only=True)
    users = UserSerializer(many=True, read_only=True) 
    user_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=User.objects.all(), source='users'
    ) 

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by', 'users', 'user_ids']
        read_only_fields = ['created_at', 'created_by'] # These are set automatically


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for Project details including client name for specific output"""
    client = serializers.StringRelatedField(read_only=True) # Show client name
    created_by = serializers.StringRelatedField(read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for basic Client List/Create/Update"""
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'created_by', 'updated_at']


class ClientDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed Client view including projects"""
    created_by = serializers.StringRelatedField(read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'created_by', 'updated_at', 'projects']