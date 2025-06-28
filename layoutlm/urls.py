from django.urls import path
from .api import LayoutLMDocumentAPI

urlpatterns = [
    path('api/layoutlm/', LayoutLMDocumentAPI.as_view(), name='layoutlm-api'),
]
