from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('upload/', views.upload_document, name='upload'),
    path('extract-custom/', views.extract_custom_fields, name='extract_custom'),
    path('multi-technique/', views.multi_technique_analysis, name='multi_technique'),
    path('api/techniques/', views.get_techniques, name='get_techniques'),
    path('api/health/', views.health_check, name='health'),
]