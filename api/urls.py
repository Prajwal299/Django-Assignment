# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')


urlpatterns = [
    path('', include(router.urls)), 
    path('clients/<int:client_pk>/projects/', views.ProjectCreateAPIView.as_view(), name='client-project-create'),
    path('projects/', views.UserProjectListAPIView.as_view(), name='user-project-list'),
]