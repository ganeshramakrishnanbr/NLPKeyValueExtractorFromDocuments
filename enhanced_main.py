"""
Enhanced Document Processing API
FastAPI backend with advanced document processing capabilities
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tempfile
import os
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional

from core.document_processor import EnhancedDocumentProcessor, ProcessingOptions, ProcessingResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Enhanced Document Processing API",
    description="Advanced document processing with OCR, table extraction, and multi-format support",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Enhanced API root endpoint"""
    return {
        "message": "Enhanced Document Processing API",
        "version": "2.0.0",
        "features": [
            "Multi-format document support (PDF, DOCX, HTML, TXT)",
            "OCR processing with Tesseract",
            "Table extraction from PDFs",
            "Image processing and enhancement",
            "Document quality assessment",
            "Batch processing support"
        ],
        "endpoints": {
            "upload": "/upload-enhanced/",
            "batch": "/batch-process/",
            "health": "/health-enhanced"
        }
    }

@app.get("/health-enhanced")
async def health_check():
    """Enhanced health check with component status"""
    try:
        # Initialize processor to test components
        processor = EnhancedDocumentProcessor()
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "components": {
                "pdf_processor": "ready",
                "docx_processor": "ready", 
                "html_processor": "ready",
                "txt_processor": "ready",
                "ocr_processor": "ready",
                "table_extractor": "ready",
                "image_processor": "ready",
                "quality_assessor": "ready"
            },
            "supported_formats": ["PDF", "DOCX", "DOC", "HTML", "TXT"],
            "features": ["OCR", "Table Extraction", "Image Processing", "Quality Assessment"]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.post("/upload-enhanced/")
async def upload_enhanced_document(
    file: UploadFile = File(...),
    enable_ocr: bool = Form(True),
    extract_tables: bool = Form(True),
    extract_images: bool = Form(True),
    enhance_images: bool = Form(True),
    perform_quality_check: bool = Form(True),
    ocr_languages: str = Form("en"),
    confidence_threshold: float = Form(0.7)
):
    """Enhanced document upload with advanced processing options"""
    
    try:
        # Parse OCR languages
        languages = [lang.strip() for lang in ocr_languages.split(',')]
        
        # Create processing options
        options = ProcessingOptions(
            enable_ocr=enable_ocr,
            extract_tables=extract_tables,
            extract_images=extract_images,
            enhance_images=enhance_images,
            perform_quality_check=perform_quality_check,
            ocr_languages=languages,
            confidence_threshold=confidence_threshold
        )
        
        # Initialize enhanced processor
        processor = EnhancedDocumentProcessor(options)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Process document
            result = await processor.process_document(tmp_file_path)
            
            # Convert to response format
            response = {
                "document_type": result.document_type.value,
                "text_content": result.text_content,
                "metadata": result.metadata,
                "tables": result.tables,
                "images": result.images,
                "quality_score": result.quality_score,
                "ocr_confidence": result.ocr_confidence,
                "processing_time": result.processing_time,
                "errors": result.errors,
                "processing_options": {
                    "ocr_enabled": enable_ocr,
                    "tables_extracted": extract_tables,
                    "images_processed": extract_images,
                    "quality_assessed": perform_quality_check
                }
            }
            
            return response
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        logger.error(f"Enhanced document processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/batch-process/")
async def batch_process_documents(files: List[UploadFile] = File(...)):
    """Process multiple documents concurrently"""
    
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
        
        # Initialize processor
        processor = EnhancedDocumentProcessor()
        
        # Save all files temporarily
        temp_files = []
        try:
            for file in files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
                    content = await file.read()
                    tmp_file.write(content)
                    temp_files.append((tmp_file.name, file.filename))
            
            # Process all documents
            file_paths = [temp_file[0] for temp_file in temp_files]
            results = await processor.process_batch(file_paths)
            
            # Format response
            batch_response = {
                "batch_id": f"batch_{int(time.time())}",
                "total_files": len(files),
                "processed_files": len(results),
                "processing_time": sum(result.processing_time for result in results),
                "results": []
            }
            
            for i, result in enumerate(results):
                file_result = {
                    "filename": temp_files[i][1],
                    "document_type": result.document_type.value,
                    "text_length": len(result.text_content),
                    "tables_found": len(result.tables),
                    "images_found": len(result.images),
                    "quality_score": result.quality_score,
                    "processing_time": result.processing_time,
                    "success": len(result.errors) == 0,
                    "errors": result.errors
                }
                batch_response["results"].append(file_result)
            
            return batch_response
            
        finally:
            # Clean up all temporary files
            for temp_file, _ in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

@app.get("/processing-stats")
async def get_processing_stats():
    """Get processing capabilities and statistics"""
    return {
        "supported_formats": {
            "pdf": {
                "description": "PDF documents with text and image extraction",
                "features": ["text extraction", "table extraction", "OCR", "metadata"]
            },
            "docx": {
                "description": "Microsoft Word documents",
                "features": ["text extraction", "table extraction", "metadata"]
            },
            "html": {
                "description": "HTML web pages",
                "features": ["text extraction", "metadata", "link analysis"]
            },
            "txt": {
                "description": "Plain text files",
                "features": ["text extraction", "encoding detection", "content analysis"]
            }
        },
        "ocr_capabilities": {
            "engine": "Tesseract",
            "supported_languages": ["eng", "fra", "deu", "spa", "ita", "por"],
            "features": ["image enhancement", "confidence scoring", "multi-language"]
        },
        "performance": {
            "typical_processing_time": "1-5 seconds per document",
            "max_batch_size": 10,
            "max_file_size": "50MB per file"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)