# Enhanced Document Processing Engine

A sophisticated Python-powered document intelligence platform that combines FastAPI and Django for advanced local NLP-driven information extraction and web-based document processing with multi-format support and enhanced OCR capabilities.

## 🏗️ Architecture & Technology Stack

This application uses a **hybrid multi-service architecture** with advanced document processing capabilities:

### High-Level Architecture
- **Frontend**: Django-based rich dashboard with Bootstrap 5 UI and proxy routing
- **Standard API**: FastAPI NLP processing engine for basic extraction
- **Enhanced API**: Advanced document processor with OCR, table extraction, and image processing
- **Communication**: Django proxy endpoints for seamless API integration
- **Processing**: Entirely local - no external API dependencies, enhanced privacy and security

### Project Directory Structure

```
enhanced-document-processing/
├── 📁 core/                       # Enhanced Document Processing Engine
│   ├── document_processor.py      # Main processing engine with multi-format support
│   ├── image_processor.py         # Image extraction and enhancement
│   ├── ocr_processor.py           # Tesseract OCR processing
│   ├── table_extractor.py         # PDF table extraction using pdfplumber
│   └── quality_assessor.py        # Document quality assessment
│
├── 📁 processors/                 # Format-Specific Processors
│   ├── pdf_processor.py           # PDF processing with pdfplumber and PyMuPDF
│   ├── docx_processor.py          # DOCX/DOC processing with python-docx
│   ├── html_processor.py          # HTML processing with BeautifulSoup
│   └── txt_processor.py           # Text file processing with encoding detection
│
├── 📁 models/                     # Enhanced Data Models
│   └── document_models.py         # Comprehensive Pydantic models
│
├── 📁 frontend/                   # Django Frontend Application
│   ├── 📁 dashboard/              # Main dashboard Django app
│   │   ├── views.py               # Frontend views
│   │   ├── proxy_views.py         # API proxy endpoints for connectivity
│   │   ├── proxy_urls.py          # Proxy URL routing
│   │   ├── urls.py                # Frontend URL routing
│   │   └── templates/             # HTML templates with enhanced UI
│   ├── 📁 config/                 # Django project configuration
│   │   ├── settings.py            # Django settings with CORS
│   │   └── urls.py                # Root URL configuration with proxy routing
│   └── manage.py                  # Django management script
│
├── 📁 utils/                      # Utility Functions
├── 📁 tests/                      # Test Suite
├── 📁 docs/                       # Documentation
│
├── 📄 main_simple.py              # Standard FastAPI backend (port 8000)
├── 📄 enhanced_simple.py          # Enhanced FastAPI backend (port 8001)
├── 📄 enhanced_main.py            # Full-featured enhanced API
├── 📄 pyproject.toml              # Python project dependencies
└── 📄 README.md                   # This documentation file
```

### Folder Structure Explained

#### 🔧 `/backend/` - FastAPI Backend Services
The core NLP processing engine that handles all document analysis and field extraction.

- **`/models/`**: Contains Pydantic data models that define API request/response schemas and data validation
- **`/processors/`**: Document processing engines that extract text from various file formats (PDF, DOCX, DOC, MD)
- **`/extractors/`**: Field extraction algorithms using pattern matching, fuzzy matching, and contextual analysis
- **`/classifiers/`**: Machine learning classification components for document recognition and confidence scoring
- **`/utils/`**: Backend utility functions and helper modules

#### 🎨 `/frontend/` - Django Frontend Application  
The user-facing web interface that provides a rich dashboard experience.

- **`/dashboard/`**: Main Django application containing views, templates, and URL routing
- **`/static/`**: Static web assets including CSS stylesheets, JavaScript files, and images
- **`/config/`**: Django project configuration files including settings and WSGI configuration
- **Database files**: SQLite database for Django application state

#### 🔄 `/shared/` - Common Components
Shared utilities and models used by both frontend and backend services.

- **`/models/`**: Common data models shared between services
- **`/utils/`**: Utility functions used across the application

#### 📚 `/docs/` - Documentation Hub
Comprehensive documentation including user guides and development notes.

- **`/prompts/`**: **NEW**: Timestamped logs of all user prompts and interactions for development tracking
- **`/guides/`**: User guides, tutorials, and how-to documentation  
- **`/architecture/`**: Technical architecture documentation and system design notes

## ✨ Features

### Rich Dashboard Interface
- **Modern Bootstrap 5 UI**: Professional, responsive design with dark/light theme support
- **Real-time API Status**: Live connectivity monitoring with visual indicators
- **Interactive Processing Modes**: Standard, Custom Fields, Multi-Technique, Enhanced options
- **Drag & Drop Upload**: Intuitive file upload with real-time validation
- **Progress Tracking**: Visual feedback during document processing with detailed logs
- **Results Visualization**: Comprehensive display of extracted data with confidence scores

### Core Processing Capabilities
- **Multi-Format Document Support**: PDF, DOCX, DOC, HTML, TXT, RTF files
- **Four Processing Modes**:
  - **Standard Processing**: Extract predefined common fields (name, address, phone, email, etc.)
  - **Custom Field Extraction**: User-specified comma-separated field extraction
  - **Multi-Technique Analysis**: Comparative analysis showing all 6 extraction techniques
  - **Enhanced Processing**: Advanced features with OCR, table extraction, image processing
- **Django Proxy Architecture**: Seamless API connectivity through proxy endpoints
- **Local NLP Processing**: No external API dependencies for maximum privacy and security
- **Advanced Pattern Recognition**: Enhanced regex, fuzzy matching, and contextual analysis

### Enhanced Processing Features
- **OCR Capabilities**: Tesseract-based text extraction from images and scanned documents
- **Table Extraction**: Automatic table detection and extraction from PDF documents
- **Image Processing**: Image extraction, enhancement, and quality assessment
- **Quality Assessment**: Document processing quality scoring and validation
- **Multi-format Support**: PDF, DOCX, DOC, HTML, TXT with encoding detection
- **Metadata Extraction**: Comprehensive document metadata and properties
- **Batch Processing**: Concurrent processing of multiple documents

### Multi-Technique Analysis (6 Techniques)
1. **Regex Pattern Matching** - Structured data identification with pattern validation
2. **NLP Processing** - Natural language processing for contextual extraction
3. **Fuzzy Matching** - Approximate string matching with similarity scoring
4. **Proximity Analysis** - Distance-based value extraction around keywords
5. **Template Matching** - Document structure and layout pattern recognition
6. **Confidence Ensemble** - Combined technique approach with weighted confidence scoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- FastAPI with Uvicorn
- All dependencies are automatically managed via the packager

### Installation
The system uses modern Python dependency management - all required packages are automatically installed:

**Core Dependencies:**
- Django, FastAPI, Uvicorn for web frameworks
- pdfplumber, PyMuPDF for PDF processing
- python-docx, docx2txt for DOCX/DOC processing
- BeautifulSoup4 for HTML processing
- pytesseract, opencv-python for OCR capabilities
- Pillow for image processing
- requests for API proxy functionality
- fuzzywuzzy, python-levenshtein for fuzzy matching

### Run the Application (3 Services Architecture)

The system runs three concurrent services for optimal performance:

```bash
# Service 1: Standard FastAPI Backend (Port 8000)
python main_simple.py

# Service 2: Enhanced Document API (Port 8001) 
python enhanced_simple.py

# Service 3: Django Frontend with Proxy (Port 5000)
cd frontend && python manage.py runserver 0.0.0.0:5000
```

### Access Points
- **Main Application**: `http://localhost:5000` - Django Dashboard with full UI
- **Standard API**: `http://localhost:8000` - Basic document processing
- **Enhanced API**: `http://localhost:8001` - Advanced processing with OCR/tables
- **API Documentation**: `http://localhost:8000/docs` and `http://localhost:8001/docs`
- **Proxy Health Check**: `http://localhost:5000/api/health/` - Combined system status

> **Important**: Use `http://localhost:5000` for the web interface. The Django frontend includes proxy endpoints at `/api/` that route to the appropriate backend services.

## 📁 Project Structure

```
nlp-document-extraction/
├── main_simple.py              # FastAPI backend application
├── manage.py                   # Django management script
├── dashboard/                  # Django frontend application
│   ├── views.py               # Frontend views and API proxying
│   ├── urls.py                # URL routing
│   └── templates/             # HTML templates
├── static/                    # Static assets (CSS, JS, images)
│   ├── css/dashboard.css      # Modern dashboard styling
│   └── js/dashboard.js        # Interactive functionality
├── nlp_dashboard/             # Django project settings
├── templates/                 # FastAPI templates (legacy)
├── docs/                      # Documentation files
├── advanced_models.py         # Pydantic models for advanced features
├── models.py                  # Basic Pydantic models
├── document_processor.py      # Multi-format document processing
├── simple_extractor.py        # Dynamic field extraction engine
├── multi_technique_extractor_simple.py  # Multi-technique analysis
├── template_classifier.py     # Document template classification
├── confidence_scorer.py       # Advanced confidence scoring
└── README.md                  # This file
```

## 🔧 Core Components

### Enhanced Processing Engine (`core/`)

#### 1. Document Processor (`core/document_processor.py`)
- **Multi-format Support**: PDF, DOCX, DOC, HTML, TXT, RTF
- **Processing Options**: OCR, table extraction, image processing, quality assessment
- **Async Processing**: Concurrent document processing for improved performance
- **Quality Assessment**: Automatic quality scoring and OCR confidence measurement

#### 2. Image Processor (`core/image_processor.py`)
- **Image Extraction**: Extract images from PDF documents and standalone image files
- **Quality Enhancement**: Automatic image enhancement for better OCR results
- **Quality Assessment**: Image quality metrics including sharpness, brightness, contrast
- **Format Support**: JPEG, PNG with comprehensive metadata extraction

#### 3. OCR Processor (`core/ocr_processor.py`)
- **Tesseract Integration**: Advanced OCR using Tesseract engine
- **Image Enhancement**: Pre-processing for optimal OCR accuracy
- **Multi-language Support**: Configurable language support for OCR
- **Confidence Scoring**: OCR confidence assessment and quality metrics

#### 4. Table Extractor (`core/table_extractor.py`)
- **PDF Table Extraction**: Automatic table detection and extraction using pdfplumber
- **Data Cleaning**: Advanced table data processing and cleaning
- **Multiple Formats**: CSV string and JSON records output
- **Header Detection**: Automatic table header identification

### Format-Specific Processors (`processors/`)

#### 1. PDF Processor (`processors/pdf_processor.py`)
- **Multiple Libraries**: pdfplumber for text, PyMuPDF for metadata
- **Text Extraction**: High-quality text extraction with fallback methods
- **Metadata Extraction**: Comprehensive PDF metadata including creation date, author
- **Page Counting**: Accurate page count and document structure analysis

#### 2. DOCX Processor (`processors/docx_processor.py`)
- **python-docx Integration**: Native DOCX and DOC file processing
- **Text Extraction**: Complete text extraction including headers, footers
- **Metadata Support**: Document properties and creation information
- **Error Handling**: Robust handling of corrupted or password-protected files

#### 3. HTML Processor (`processors/html_processor.py`)
- **BeautifulSoup Integration**: Advanced HTML parsing and cleaning
- **Encoding Detection**: Automatic encoding detection for international content
- **Clean Text Extraction**: Removal of HTML tags while preserving structure
- **Metadata Extraction**: Title, description, and HTML meta information

### Django Frontend with Proxy (`frontend/`)

#### 1. Proxy System (`frontend/dashboard/proxy_views.py`)
- **API Routing**: Intelligent routing to appropriate backend services
- **Error Handling**: Comprehensive error handling with detailed logging
- **File Upload Support**: Seamless file upload proxying with progress tracking
- **Health Monitoring**: Combined health checks across all services

#### 2. Enhanced UI (`frontend/templates/dashboard/home.html`)
- **Dynamic API Detection**: Automatic API endpoint detection and connectivity testing
- **Multi-Mode Processing**: Standard, Custom, Multi-Technique, and Enhanced processing modes
- **Real-time Feedback**: Live status updates and progress tracking
- **Results Visualization**: Comprehensive display of processing results and confidence scores

## 📊 Usage Examples

### Standard Processing Mode
Upload any supported document format and automatically extract common fields:
- **Personal Information**: Names, addresses, phone numbers, email addresses
- **Dates**: Birth dates, issue dates, expiration dates
- **Financial Data**: Policy numbers, amounts, premiums
- **Document Type**: Automatic classification and confidence scoring

### Custom Field Extraction
Define your own extraction fields using comma-separated values:
```
policy_number, issue_date, coverage_amount, premium, beneficiary_name, ssn, date_of_birth
```

### Multi-Technique Analysis
Compare results from all 6 extraction techniques with individual confidence scores:
- **Regex Pattern Matching**: 95% confidence
- **NLP Processing**: 87% confidence  
- **Fuzzy Matching**: 92% confidence
- **Proximity Analysis**: 89% confidence
- **Template Matching**: 91% confidence
- **Confidence Ensemble**: 93% confidence (recommended)

### Enhanced Processing Features
Enable advanced capabilities for complex documents:
- **OCR Processing**: Extract text from scanned documents and images
- **Table Extraction**: Automatically detect and extract tables from PDFs
- **Image Processing**: Extract and enhance images with quality assessment
- **Quality Assessment**: Overall document processing quality scoring
- **Batch Processing**: Process multiple documents concurrently

### Typical Workflow
1. **Upload Document**: Drag and drop or select file (PDF, DOCX, HTML, TXT)
2. **Select Processing Mode**: Choose Standard, Custom, Multi-Technique, or Enhanced
3. **Configure Options**: Enable OCR, tables, images as needed
4. **Process Document**: Real-time progress tracking with status updates
5. **Review Results**: Comprehensive results with confidence scores and extracted data
6. **Download/Export**: Results available in JSON format with detailed metadata

## 🔍 API Endpoints

### Django Frontend with Proxy (`http://localhost:5000`)
- `/` - Main dashboard interface with full UI
- `/api/test/` - API connectivity test (proxied)
- `/api/health/` - Combined system health check (proxied)
- `/api/upload/` - Standard document processing (proxied to port 8000)
- `/api/extract-custom/` - Custom field extraction (proxied to port 8000)
- `/api/upload-enhanced/` - Enhanced processing with OCR/tables (proxied to port 8001)

### Standard FastAPI Backend (`http://localhost:8000`)
- `POST /upload/` - Standard field extraction
- `POST /extract-custom/` - Custom field extraction with user-defined fields
- `GET /test` - API connectivity test
- `GET /health` - Basic health check
- `GET /docs` - Swagger API documentation

### Enhanced FastAPI Backend (`http://localhost:8001`)
- `POST /upload-enhanced/` - Advanced processing with OCR, tables, images
- `POST /batch-process/` - Concurrent batch processing of multiple documents
- `GET /processing-stats/` - Processing capabilities and statistics
- `GET /health` - Enhanced health check
- `GET /docs` - Enhanced API documentation

### Proxy Architecture Benefits
- **Seamless Connectivity**: No CORS issues or external domain resolution problems
- **Unified Interface**: Single entry point through Django frontend
- **Load Distribution**: Requests automatically routed to appropriate backend service
- **Error Handling**: Comprehensive error handling and logging at proxy level

## 🛠️ Configuration

### Environment Variables
- `DEBUG`: Django debug mode (default: True)
- `ALLOWED_HOSTS`: Django allowed hosts (default: ['*'])
- `FASTAPI_BASE_URL`: FastAPI backend URL (default: http://localhost:8000)

### File Upload Limits
- Maximum file size: 50MB
- Supported formats: PDF, DOCX, DOC, MD
- Concurrent uploads: Unlimited

## 🧪 Testing

### Manual Testing
1. Start both servers (Django + FastAPI)
2. Navigate to `http://localhost:5000`
3. Upload test documents in different formats
4. Try all three processing modes
5. Verify results and confidence scores

### API Testing
Use the built-in Swagger UI at `http://localhost:8000/docs` to test API endpoints directly.

## 🔒 Security Features

- **Local Processing**: No data sent to external services
- **File Validation**: Strict file type and size validation
- **Error Handling**: Comprehensive error handling and logging
- **CORS Configuration**: Proper cross-origin request handling
- **Input Sanitization**: Protection against malicious inputs

## 📈 Performance & Technical Specifications

### Processing Performance
- **Standard Processing**: 1-3 seconds per document (text extraction only)
- **Enhanced Processing**: 3-8 seconds per document (with OCR, tables, images)
- **OCR Processing**: 5-15 seconds per document (depends on image quality and size)
- **Batch Processing**: Concurrent processing of up to 10 documents simultaneously
- **Memory Usage**: Optimized for documents up to 50MB per file

### Supported File Formats
- **PDF**: Full support including scanned PDFs with OCR
- **DOCX/DOC**: Microsoft Word documents with metadata
- **HTML**: Web pages with encoding detection
- **TXT**: Plain text files with automatic encoding detection
- **RTF**: Rich Text Format documents
- **Images**: JPEG, PNG for OCR processing

### System Requirements
- **Python**: 3.8+ (tested with 3.11)
- **Memory**: Minimum 2GB RAM, recommended 4GB for large documents
- **Storage**: 100MB for dependencies, additional space for document processing
- **Tesseract**: Automatically configured for OCR capabilities
- **Network**: No external API dependencies, fully local processing

### Scalability Features
- **Async Processing**: Non-blocking document processing with concurrent handling
- **Proxy Architecture**: Load distribution across multiple backend services
- **Error Recovery**: Robust error handling with detailed logging and recovery mechanisms
- **Health Monitoring**: Real-time system health monitoring with automatic status checking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with comprehensive comments
4. Test thoroughly across all processing modes
5. Submit a pull request with detailed description

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, bug reports, or feature requests:
- Create an issue in the repository
- Review the API documentation at `/docs`
- Check the health endpoints for system status

## 🔄 Version History

- **v3.0.0**: Enhanced Document Processing Engine
  - Added comprehensive OCR capabilities with Tesseract integration
  - Implemented table extraction from PDF documents
  - Added image processing and quality assessment
  - Introduced Django proxy architecture for seamless connectivity
  - Enhanced multi-format support (PDF, DOCX, HTML, TXT, RTF)
  - Added batch processing for concurrent document handling
  - Improved error handling and system monitoring

- **v2.0.0**: Django Frontend Integration
  - Django-based rich dashboard with Bootstrap 5 UI
  - Multi-technique analysis with 6 extraction methods
  - Real-time API status monitoring
  - Advanced confidence scoring and quality assessment

- **v1.0.0**: Initial FastAPI Backend
  - Basic document extraction capabilities
  - Standard and custom field extraction
  - Core NLP processing engine

---

**NLP Document Extraction Platform** - Intelligent document processing with advanced NLP capabilities.