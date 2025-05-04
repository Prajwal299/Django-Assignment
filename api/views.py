# api/views.py
from rest_framework import generics, viewsets, status
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
    API endpoint that allows clients to be viewed or edited.
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
        serializer.save(client=client_instance, created_by=self.request.user)

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) 

        instance = serializer.instance
        output_serializer = ProjectDetailSerializer(instance, context=self.get_serializer_context())

        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserProjectListAPIView(generics.ListAPIView):
    """
    API endpoint to list projects assigned to the logged-in user.
    GET /api/projects/
    """
    serializer_class = ProjectDetailSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.projects.all().order_by('-created_at') 