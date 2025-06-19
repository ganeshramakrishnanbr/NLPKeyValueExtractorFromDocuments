from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import requests
import tempfile
import os

# FastAPI backend URL
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
    """Handle standard document upload"""
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

@csrf_exempt
@require_http_methods(["POST"])
def multi_technique_analysis(request):
    """Handle multi-technique analysis"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        uploaded_file = request.FILES['file']
        selected_techniques = request.POST.get('selected_techniques', '')
        fields = request.POST.get('fields', '')
        
        # Forward to FastAPI backend
        files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)}
        data = {
            'selected_techniques': selected_techniques,
            'fields': fields
        }
        response = requests.post(f"{FASTAPI_BASE_URL}/upload/multi-technique/", files=files, data=data)
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Processing failed'}, status=response.status_code)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_techniques(request):
    """Get available extraction techniques"""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/techniques/")
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Failed to get techniques'}, status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def health_check(request):
    """Health check endpoint"""
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/health")
        backend_status = response.status_code == 200
        
        return JsonResponse({
            'status': 'healthy' if backend_status else 'degraded',
            'frontend': 'Django Dashboard',
            'backend': 'FastAPI NLP Engine',
            'backend_status': backend_status
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
