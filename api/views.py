# api/views.py
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # Require users to be logged in
from django.shortcuts import get_object_or_404

from .models import Client, Project
from .serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ProjectSerializer,
    ProjectDetailSerializer # Used for the user's project list maybe?
)
from django.contrib.auth.models import User

# Using ViewSets for Client CRUD - combines List, Create, Retrieve, Update, Delete
class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    permission_classes = [IsAuthenticated] # Only logged-in users can access

    def get_queryset(self):
        # Return all clients - could add filtering by user later if needed
        return Client.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        # Use detail serializer for retrieve action, otherwise use standard one
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        # Automatically set the created_by field to the logged-in user
        serializer.save(created_by=self.request.user)

# Specific Views for Projects because of nested URL and custom logic

class ProjectCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create a project for a specific client.
    POST /api/clients/<client_pk>/projects/
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        client_pk = self.kwargs.get('client_pk')
        client_instance = get_object_or_404(Client, pk=client_pk)
        # Check if client exists happens via get_object_or_404
        # Assign client and created_by user automatically
        serializer.save(client=client_instance, created_by=self.request.user)

    # Customizing the response to match the desired output format
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) # Saves the instance

        # Re-serialize the created instance using the detail serializer for output
        # We need client name and nested users in the output
        instance = serializer.instance # Get the saved project instance
        output_serializer = ProjectDetailSerializer(instance, context=self.get_serializer_context())

        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserProjectListAPIView(generics.ListAPIView):
    """
    API endpoint to list projects assigned to the logged-in user.
    GET /api/projects/
    """
    serializer_class = ProjectDetailSerializer # Use serializer that includes client name
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter projects where the logged-in user is in the 'users' list
        user = self.request.user
        return user.projects.all().order_by('-created_at') # Access via related_name='projects' on User