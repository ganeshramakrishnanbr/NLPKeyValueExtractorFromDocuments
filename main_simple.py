from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import tempfile
import os
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from models import ExtractionResult, CustomerInfo, PolicyInfo, DynamicExtractionResult
from advanced_models import (
    AdvancedExtractionResult, TemplateListResponse, StateRequirementsResponse,
    TemplateLearnRequest, TemplateLearnResponse, HealthCheckAdvanced, APIInfoAdvanced
)
from document_processor import DocumentProcessor
from simple_extractor import SimpleDynamicExtractor
from template_classifier import AdvancedTemplateClassifier
from confidence_scorer import EnhancedConfidenceScorer

app = FastAPI(
    title="NLP Key Value Extractor From Documents", 
    version="1.0.0",
    description="Extract key-value information from PDF, DOCX, DOC, and Markdown files using intelligent pattern recognition"
)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize processors
document_processor = DocumentProcessor()
dynamic_extractor = SimpleDynamicExtractor()

# Initialize Phase 2 advanced components
template_classifier = AdvancedTemplateClassifier()
confidence_scorer = EnhancedConfidenceScorer()

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
        allowed_extensions = {'.pdf', '.docx', '.doc', '.md'}
        
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
async def extract_custom_fields(file: UploadFile = File(...), fields: str = Form("")):
    """
    Upload and process documents (PDF, DOCX, DOC, MD) with custom field extraction.
    Specify which fields to extract in the 'fields' parameter as comma-separated values.
    """
    start_time = time.time()
    
    # Parse the fields parameter - use exactly what user requests
    logger.info(f"Raw fields parameter received: '{fields}'")
    logger.info(f"Fields strip check: '{fields.strip()}' - Length: {len(fields.strip())}")
    
    if fields and fields.strip():
        field_list = [field.strip() for field in fields.split(',') if field.strip()]
        logger.info(f"CUSTOM FIELDS PARSED: {field_list}")
    else:
        # Only use defaults if no fields specified at all
        field_list = ['name', 'email', 'phone', 'address', 'date', 'company', 'amount']
        logger.info(f"USING DEFAULT FIELDS: {field_list}")
    
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = {'.pdf', '.docx', '.doc', '.md'}
        
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
            logger.info(f"Passing field_list to extractor: {field_list}")
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

@app.post("/upload/advanced/", response_model=AdvancedExtractionResult)
async def upload_document_advanced(file: UploadFile = File(...), fields: str = Form("")):
    """
    Enhanced processing with advanced NLP, template recognition, and state compliance
    """
    start_time = time.time()
    
    # Parse fields parameter
    if fields and fields.strip():
        field_list = [field.strip() for field in fields.split(',') if field.strip()]
        logger.info(f"Advanced processing with custom fields: {field_list}")
    else:
        field_list = ['name', 'email', 'phone', 'address', 'date', 'company', 'amount']
        logger.info(f"Advanced processing with default fields: {field_list}")
    
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = {'.pdf', '.docx', '.doc', '.md'}
        
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
            # Step 1: Extract text from document
            extracted_text = document_processor.extract_text(
                temp_file_path, 
                file_extension[1:]
            )
            
            if not extracted_text.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the document")
            
            # Step 2: Advanced template classification
            template_classification = template_classifier.classify_document_advanced(extracted_text)
            
            # Step 3: Extract custom fields using existing extractor
            extracted_fields = dynamic_extractor.extract_custom_fields(extracted_text, field_list)
            
            # Step 4: Enhanced confidence scoring
            confidence_analysis = confidence_scorer.calculate_ensemble_confidence(
                {"extracted_fields": extracted_fields},
                template_classification,
                {"processing_time": time.time() - start_time}
            )
            
            # Step 5: Calculate processing time
            processing_time = round(time.time() - start_time, 2)
            
            # Step 6: Create preview
            raw_text_preview = extracted_text[:200].strip()
            if len(extracted_text) > 200:
                raw_text_preview += "..."
            
            # Create advanced result
            result = AdvancedExtractionResult(
                document_type=template_classification["primary_category"],
                sub_category=template_classification["sub_category"],
                extracted_fields=extracted_fields,
                template_classification=template_classification,
                confidence_analysis=confidence_analysis,
                state_regulations=template_classification["state_regulations"],
                organizations=template_classification["organizations"],
                processing_time=processing_time,
                complexity_score=template_classification["complexity_score"],
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
            detail=f"Error in advanced processing: {str(e)}"
        )

@app.get("/templates/", response_model=TemplateListResponse)
async def list_available_templates():
    """List all available template categories and information"""
    try:
        template_info = template_classifier.get_available_templates()
        
        # Convert to proper response format
        custom_templates = []
        for template_name in template_info.get("custom_templates", []):
            custom_templates.append({
                "template_name": template_name,
                "category": "custom",
                "keywords": [],
                "complexity": 0.5
            })
        
        return TemplateListResponse(
            primary_categories=template_info["primary_categories"],
            state_coverage=template_info["state_coverage"],
            known_organizations=template_info["known_organizations"],
            custom_templates=custom_templates,
            total_templates=len(template_info["primary_categories"]) + len(custom_templates)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")

@app.post("/templates/learn/", response_model=TemplateLearnResponse)
async def learn_new_template(request: TemplateLearnRequest):
    """Teach the system to recognize new document templates"""
    try:
        success = template_classifier.learn_new_template(
            request.sample_text, 
            request.template_name,
            request.category
        )
        
        if success:
            # Extract keywords for response
            keywords = template_classifier._extract_template_keywords(request.sample_text)
            
            return TemplateLearnResponse(
                success=True,
                template_name=request.template_name,
                extracted_keywords=keywords,
                message=f"Successfully learned template: {request.template_name}"
            )
        else:
            return TemplateLearnResponse(
                success=False,
                template_name=request.template_name,
                extracted_keywords=[],
                message="Failed to learn template"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error learning template: {str(e)}")

@app.get("/state-requirements/{state}", response_model=StateRequirementsResponse)
async def get_state_requirements(state: str):
    """Get document requirements for specific state"""
    try:
        state_lower = state.lower().replace(" ", "_")
        requirements = template_classifier._get_state_requirements(state_lower)
        
        if not requirements:
            raise HTTPException(status_code=404, detail=f"No requirements found for state: {state}")
        
        # Map state to regulatory authority
        regulatory_authorities = {
            "california": "California Department of Insurance",
            "new_york": "New York Department of Financial Services",
            "texas": "Texas Department of Insurance",
            "florida": "Florida Office of Insurance Regulation"
        }
        
        return StateRequirementsResponse(
            state=state_lower,
            requirements=requirements,
            compliance_level="Standard" if state_lower not in ["california", "new_york"] else "Strict",
            regulatory_authority=regulatory_authorities.get(state_lower, f"{state} Department of Insurance")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving state requirements: {str(e)}")

@app.get("/health/advanced", response_model=HealthCheckAdvanced)
async def health_check_advanced():
    """Enhanced health check with advanced feature status"""
    try:
        # Check advanced feature availability
        advanced_features = {
            "template_classification": True,
            "confidence_scoring": True,
            "state_compliance": True,
            "organization_detection": True
        }
        
        template_info = template_classifier.get_available_templates()
        
        return HealthCheckAdvanced(
            status="healthy",
            message="Advanced NLP Key Value Extractor is running with all features",
            timestamp=time.time(),
            advanced_features=advanced_features,
            template_count=len(template_info["primary_categories"]),
            supported_states=len(template_info["state_coverage"])
        )
    except Exception as e:
        return HealthCheckAdvanced(
            status="degraded",
            message=f"Advanced features partially available: {str(e)}",
            timestamp=time.time(),
            advanced_features={"template_classification": False, "confidence_scoring": False, "state_compliance": False, "organization_detection": False},
            template_count=0,
            supported_states=0
        )

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "NLP Key Value Extractor From Documents API - Phase 2 Enhanced",
        "version": "2.0.0",
        "supported_formats": ["PDF", "DOCX", "DOC", "MD"],
        "endpoints": {
            "upload": "/upload/ (POST) - Upload and process documents with preset fields",
            "extract-custom": "/extract-custom/ (POST) - Upload and extract custom fields",
            "upload-advanced": "/upload/advanced/ (POST) - Advanced processing with template recognition",
            "templates": "/templates/ (GET) - List available templates",
            "templates-learn": "/templates/learn/ (POST) - Learn new templates",
            "state-requirements": "/state-requirements/{state} (GET) - Get state requirements",
            "health": "/health (GET) - Basic health check",
            "health-advanced": "/health/advanced (GET) - Advanced feature health check",
            "docs": "/docs - API documentation"
        },
        "advanced_features": [
            "Template Classification for 3,700+ document varieties",
            "State-specific regulation identification for all 50 US states", 
            "Enhanced confidence scoring with multiple algorithms",
            "Organization/carrier detection",
            "Document complexity analysis",
            "Template learning capabilities"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)