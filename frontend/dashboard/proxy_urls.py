"""
URL patterns for API proxy endpoints
"""
from django.urls import path
from . import proxy_views

urlpatterns = [
    path('test/', proxy_views.api_test, name='api_test'),
    path('health/', proxy_views.api_health, name='api_health'),
    path('upload/', proxy_views.api_upload, name='api_upload'),
    path('extract-custom/', proxy_views.api_extract_custom, name='api_extract_custom'),
    path('upload-enhanced/', proxy_views.api_upload_enhanced, name='api_upload_enhanced'),
]