# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')
# The router generates: /clients/, /clients/{pk}/ etc.

# Define specific URLs for non-viewset views
urlpatterns = [
    path('', include(router.urls)), # Include the router-generated URLs
    path('clients/<int:client_pk>/projects/', views.ProjectCreateAPIView.as_view(), name='client-project-create'),
    path('projects/', views.UserProjectListAPIView.as_view(), name='user-project-list'),
]