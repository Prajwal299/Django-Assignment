# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'projects', views.ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
