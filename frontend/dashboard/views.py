"""
Django Dashboard Views Module

This module handles all Django frontend view logic for the NLP Document Extraction
Platform. It provides rich web interface views and proxies requests to the FastAPI
backend for document processing.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import requests
import tempfile
import os

# FastAPI backend URL for API proxying
FASTAPI_BASE_URL = "http://localhost:8000"

def dashboard_home(request):
    """Main dashboard view with rich interface"""
    context = {
        'title': 'NLP Document Extraction Dashboard',
        'description': 'Advanced document processing with intelligent pattern recognition',
        'supported_formats': ['PDF', 'DOCX', 'DOC', 'MD'],
        'features': [
            'Standard preset field extraction',
            'Custom field specification',
            'Multi-technique comparative analysis',
            'Real-time confidence scoring',
            'Solution rationale explanations'
        ]
    }
    return render(request, 'dashboard/home.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def upload_document(request):
    """Handle standard document upload and processing"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Forward to FastAPI backend
        files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)}
        response = requests.post(f"{FASTAPI_BASE_URL}/upload/", files=files)
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Processing failed'}, status=response.status_code)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def extract_custom_fields(request):
    """Handle custom field extraction"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        fields = request.POST.get('fields', '')
        
        # Forward to FastAPI backend
        files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)}
        data = {'fields': fields}
        response = requests.post(f"{FASTAPI_BASE_URL}/extract-custom/", files=files, data=data)
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Processing failed'}, status=response.status_code)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def health_check(request):
    """Combined health check for both frontend and backend"""
    try:
        # Check backend health
        backend_response = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=5)
        backend_healthy = backend_response.status_code == 200
        
        return JsonResponse({
            'status': 'healthy' if backend_healthy else 'degraded',
            'frontend': 'healthy',
            'backend': 'healthy' if backend_healthy else 'unhealthy',
            'message': 'All services operational' if backend_healthy else 'Backend service unavailable'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'frontend': 'healthy',
            'backend': 'unhealthy',
            'message': f'Backend connection failed: {str(e)}'
        }, status=503)