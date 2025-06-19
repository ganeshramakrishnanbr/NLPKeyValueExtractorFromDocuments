"""
URL configuration for NLP Document Extraction Frontend
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dashboard.proxy_urls')),
    path('', include('dashboard.urls')),
]