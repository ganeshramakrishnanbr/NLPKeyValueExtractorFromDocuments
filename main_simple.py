from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import tempfile
import os
import time
from pathlib import Path
from models import ExtractionResult, CustomerInfo, PolicyInfo, DynamicExtractionResult
from document_processor import DocumentProcessor
from simple_extractor import SimpleDynamicExtractor

app = FastAPI(title="Life Insurance Document Processor", version="1.0.0")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize processors
document_processor = DocumentProcessor()
dynamic_extractor = SimpleDynamicExtractor()

@app.post("/upload/", response_model=ExtractionResult)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process life insurance documents (PDF, DOCX, DOC).
    Extracts customer and policy information using basic pattern matching.
    """
    start_time = time.time()
    
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = {'.pdf', '.docx', '.doc'}
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from document
            extracted_text = document_processor.extract_text(
                temp_file_path, 
                file_extension[1:]  # Remove the dot
            )
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the document")
            
            # Classify document type
            document_type = document_processor.classify_document_type(extracted_text)
            
            # Extract customer information using simple patterns
            customer_fields = ['name', 'ssn', 'date_of_birth', 'address', 'phone', 'email']
            customer_data = dynamic_extractor.extract_custom_fields(extracted_text, customer_fields)
            customer_info = CustomerInfo(
                name=customer_data.get('name'),
                ssn=customer_data.get('ssn'),
                date_of_birth=customer_data.get('date_of_birth'),
                address=customer_data.get('address'),
                phone=customer_data.get('phone'),
                email=customer_data.get('email')
            )
            
            # Extract policy information
            policy_fields = ['policy_number', 'policy_type', 'coverage_amount', 'premium']
            policy_data = dynamic_extractor.extract_custom_fields(extracted_text, policy_fields)
            policy_info = PolicyInfo(
                policy_number=policy_data.get('policy_number'),
                policy_type=policy_data.get('policy_type'),
                coverage_amount=policy_data.get('coverage_amount'),
                premium=policy_data.get('premium')
            )
            
            # Calculate confidence score
            all_fields = customer_fields + policy_fields
            all_extracted_data = {**customer_data, **policy_data}
            confidence_score = dynamic_extractor.calculate_confidence_score(all_extracted_data, all_fields)
            
            # Calculate processing time
            processing_time = round(time.time() - start_time, 2)
            
            # Create preview of extracted text (first 200 characters)
            raw_text_preview = extracted_text[:200].strip()
            if len(extracted_text) > 200:
                raw_text_preview += "..."
            
            # Create result
            result = ExtractionResult(
                document_type=document_type,
                customer_info=customer_info,
                policy_info=policy_info,
                confidence_score=confidence_score,
                processing_time=processing_time,
                raw_text_preview=raw_text_preview
            )
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing document: {str(e)}"
        )

@app.post("/extract-custom/", response_model=DynamicExtractionResult)
async def extract_custom_fields(file: UploadFile = File(...), fields: str = ""):
    """
    Upload and process documents with custom field extraction.
    Specify which fields to extract in the 'fields' parameter as comma-separated values.
    """
    start_time = time.time()
    
    # Parse the fields parameter
    if not fields.strip():
        # If no fields specified, use a default set of common fields
        field_list = ['name', 'email', 'phone', 'address', 'date', 'company', 'amount']
    else:
        field_list = [field.strip() for field in fields.split(',') if field.strip()]
        if not field_list:
            # Fallback to default fields if parsing fails
            field_list = ['name', 'email', 'phone', 'address', 'date', 'company', 'amount']
    
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = {'.pdf', '.docx', '.doc'}
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from document
            extracted_text = document_processor.extract_text(
                temp_file_path, 
                file_extension[1:]  # Remove the dot
            )
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the document")
            
            # Classify document type
            document_type = document_processor.classify_document_type(extracted_text)
            
            # Extract custom fields
            extracted_fields = dynamic_extractor.extract_custom_fields(extracted_text, field_list)
            
            # Calculate confidence score
            confidence_score = dynamic_extractor.calculate_confidence_score(extracted_fields, field_list)
            
            # Calculate processing time
            processing_time = round(time.time() - start_time, 2)
            
            # Create preview of extracted text (first 200 characters)
            raw_text_preview = extracted_text[:200].strip()
            if len(extracted_text) > 200:
                raw_text_preview += "..."
            
            # Create result
            result = DynamicExtractionResult(
                document_type=document_type,
                extracted_fields=extracted_fields,
                confidence_score=confidence_score,
                processing_time=processing_time,
                raw_text_preview=raw_text_preview,
                requested_fields=field_list
            )
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing document: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API status"""
    return {
        "status": "healthy",
        "message": "Life Insurance Document Processor is running",
        "timestamp": time.time()
    }

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Life Insurance Document Processor API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload/ (POST) - Upload and process documents with preset fields",
            "extract-custom": "/extract-custom/ (POST) - Upload and extract custom fields",
            "health": "/health (GET) - Health check",
            "docs": "/docs - API documentation"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)