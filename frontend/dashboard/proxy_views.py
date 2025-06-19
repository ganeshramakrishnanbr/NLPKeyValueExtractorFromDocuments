"""
Proxy views to route API calls from frontend to backend services
"""
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

# Backend API URLs
BACKEND_API_URL = "http://localhost:8000"
ENHANCED_API_URL = "http://localhost:8001"

@csrf_exempt
@require_http_methods(["GET"])
def api_test(request):
    """Proxy test endpoint"""
    try:
        response = requests.get(f"{BACKEND_API_URL}/test", timeout=5)
        return JsonResponse(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"API proxy error: {e}")
        return JsonResponse({"error": "Backend API unavailable"}, status=503)

@csrf_exempt
@require_http_methods(["GET"])
def api_health(request):
    """Proxy health endpoint"""
    try:
        response = requests.get(f"{BACKEND_API_URL}/health", timeout=5)
        return JsonResponse(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"Health check error: {e}")
        return JsonResponse({"error": "Backend API unavailable"}, status=503)

@csrf_exempt
@require_http_methods(["POST"])
def api_upload(request):
    """Proxy upload endpoint"""
    try:
        # Forward the file upload to backend API
        files = {}
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            files['file'] = (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        
        response = requests.post(f"{BACKEND_API_URL}/upload/", files=files, timeout=30)
        return JsonResponse(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"Upload proxy error: {e}")
        return JsonResponse({"error": "Upload failed"}, status=503)

@csrf_exempt
@require_http_methods(["POST"])
def api_extract_custom(request):
    """Proxy custom extraction endpoint"""
    try:
        files = {}
        data = {}
        
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            files['file'] = (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        
        if 'fields' in request.POST:
            data['fields'] = request.POST['fields']
        
        response = requests.post(f"{BACKEND_API_URL}/extract-custom/", files=files, data=data, timeout=30)
        return JsonResponse(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"Custom extraction proxy error: {e}")
        return JsonResponse({"error": "Custom extraction failed"}, status=503)

@csrf_exempt
@require_http_methods(["POST"])
def api_upload_enhanced(request):
    """Proxy enhanced upload endpoint"""
    try:
        files = {}
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            files['file'] = (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
        
        response = requests.post(f"{ENHANCED_API_URL}/upload-enhanced/", files=files, timeout=30)
        return JsonResponse(response.json(), status=response.status_code)
    except requests.RequestException as e:
        logger.error(f"Enhanced upload proxy error: {e}")
        return JsonResponse({"error": "Enhanced upload failed"}, status=503)