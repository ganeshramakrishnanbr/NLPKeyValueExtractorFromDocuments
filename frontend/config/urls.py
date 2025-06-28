"""
URL configuration for NLP Document Extraction Frontend
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('layoutlm.urls')),
    # Redirect the root URL to the main upload page for a better user experience.
    path('', RedirectView.as_view(url='/upload/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)