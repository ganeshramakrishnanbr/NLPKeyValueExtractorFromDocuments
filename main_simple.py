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

app = FastAPI(title="NLP Key Value Extractor From Documents", version="1.0.0")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize processors
document_processor = DocumentProcessor()
dynamic_extractor = SimpleDynamicExtractor()

@app.post("/upload/", response_model=ExtractionResult)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process documents (PDF, DOCX, DOC, MD).
    Extracts key-value information using NLP pattern matching.
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
            
            # Extract primary information using simple patterns
            primary_fields = ['name', 'ssn', 'date_of_birth', 'address', 'phone', 'email']
            primary_data = dynamic_extractor.extract_custom_fields(extracted_text, primary_fields)
            customer_info = CustomerInfo(
                name=primary_data.get('name'),
                ssn=primary_data.get('ssn'),
                date_of_birth=primary_data.get('date_of_birth'),
                address=primary_data.get('address'),
                phone=primary_data.get('phone'),
                email=primary_data.get('email')
            )
            
            # Extract secondary information
            secondary_fields = ['policy_number', 'account_number', 'amount', 'date']
            secondary_data = dynamic_extractor.extract_custom_fields(extracted_text, secondary_fields)
            policy_info = PolicyInfo(
                policy_number=secondary_data.get('policy_number') or secondary_data.get('account_number'),
                policy_type=document_type.replace('_', ' ').title(),
                coverage_amount=secondary_data.get('amount'),
                premium=None  # Not applicable for generic documents
            )
            
            # Calculate confidence score
            all_fields = primary_fields + secondary_fields
            all_extracted_data = {**primary_data, **secondary_data}
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
        "message": "NLP Key Value Extractor From Documents is running",
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
        "message": "NLP Key Value Extractor From Documents API",
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