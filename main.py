from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import tempfile
import os
import time
from pathlib import Path
from models import ExtractionResult, CustomerInfo, PolicyInfo
from document_processor import DocumentProcessor
from nlp_extractor import InsuranceNLPExtractor

app = FastAPI(title="Life Insurance Document Processor", version="1.0.0")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize processors
document_processor = DocumentProcessor()
nlp_extractor = InsuranceNLPExtractor()

@app.post("/upload/", response_model=ExtractionResult)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process life insurance documents (PDF, DOCX, DOC).
    Extracts customer and policy information using local NLP processing.
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
            
            # Extract customer information
            customer_data = nlp_extractor.extract_customer_info(extracted_text)
            customer_info = CustomerInfo(**customer_data)
            
            # Extract policy information
            policy_data = nlp_extractor.extract_policy_info(extracted_text)
            policy_info = PolicyInfo(**policy_data)
            
            # Calculate confidence score
            all_extracted_data = {**customer_data, **policy_data}
            confidence_score = nlp_extractor.calculate_confidence_score(all_extracted_data)
            
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
        # Clean up temp file in case of error (ignore errors during cleanup)
        pass
        
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
            "upload": "/upload/ (POST) - Upload and process documents",
            "health": "/health (GET) - Health check",
            "docs": "/docs - API documentation"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
