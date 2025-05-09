# api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Client, Project
from .serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ProjectSerializer,
    ProjectDetailSerializer
)
from django.contrib.auth.models import User

class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle Client CRUD and nested project creation.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='projects')
    def create_project(self, request, pk=None):
        """
        POST /api/clients/{client_id}/projects/
        Create a project under a specific client.
        """
        client = get_object_or_404(Client, pk=pk)
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save(client=client, created_by=request.user)

        output_serializer = ProjectDetailSerializer(project, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ViewSet):
    """
    ViewSet to list all projects assigned to the current user.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/projects/
        List projects assigned to the current user.
        """
        user = request.user
        projects = user.projects.all().order_by('-created_at')
        serializer = ProjectDetailSerializer(projects, many=True)
        return Response(serializer.data)

