from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.core.files.storage import default_storage
import os

from .processor import process_document_with_layoutlm

class LayoutLMDocumentAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=400)
        file_path = default_storage.save(file_obj.name, file_obj)
        abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
        result = process_document_with_layoutlm(abs_path)
        return Response(result)
