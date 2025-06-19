"""
URL configuration for dashboard app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('extract-custom/', views.extract_custom_fields, name='extract_custom_fields'),
    path('api/health/', views.health_check, name='health_check'),
]