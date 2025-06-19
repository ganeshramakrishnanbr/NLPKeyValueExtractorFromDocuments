# NLP Document Extraction Platform

A sophisticated full-stack application for intelligent document information extraction using advanced local NLP processing techniques, featuring a modern Django frontend and FastAPI backend.

## 🏗️ Architecture & Project Structure

This application uses a **hybrid architecture** with a well-organized modular structure:

### High-Level Architecture
- **Frontend**: Django-based rich dashboard with Bootstrap 5 UI
- **Backend**: FastAPI NLP processing engine  
- **Communication**: RESTful API integration between frontend and backend
- **Processing**: Entirely local - no external API dependencies

### Project Directory Structure

```
nlp-document-extraction/
├── 📁 backend/                    # FastAPI Backend Services
│   ├── 📁 models/                 # Data models and schemas
│   │   ├── basic_models.py        # Core Pydantic models for API responses
│   │   └── advanced_models.py     # Extended models for advanced features
│   ├── 📁 processors/             # Document processing engines
│   │   └── document_processor.py  # Multi-format text extraction (PDF, DOCX, DOC, MD)
│   ├── 📁 extractors/             # Field extraction algorithms
│   │   ├── simple_extractor.py    # Pattern-based field extraction
│   │   └── multi_technique_extractor.py  # Comparative analysis engine
│   ├── 📁 classifiers/            # ML classification components
│   │   ├── template_classifier.py # Document template recognition
│   │   └── confidence_scorer.py   # Multi-algorithm confidence scoring
│   └── 📁 utils/                  # Backend utility functions
│
├── 📁 frontend/                   # Django Frontend Application
│   ├── 📁 dashboard/              # Main dashboard Django app
│   │   ├── views.py               # Frontend views and API proxying
│   │   ├── urls.py                # URL routing configuration
│   │   ├── models.py              # Django database models
│   │   └── templates/             # HTML templates for UI
│   ├── 📁 static/                 # Static assets (CSS, JS, images)
│   │   ├── css/dashboard.css      # Modern Bootstrap 5 styling
│   │   └── js/dashboard.js        # Interactive frontend functionality
│   ├── 📁 config/                 # Django project configuration
│   │   ├── settings.py            # Django settings
│   │   ├── urls.py                # Root URL configuration
│   │   └── wsgi.py                # WSGI application entry point
│   ├── manage.py                  # Django management script
│   └── db.sqlite3                 # SQLite database file
│
├── 📁 shared/                     # Shared components across services
│   ├── 📁 models/                 # Common data models
│   └── 📁 utils/                  # Shared utility functions
│
├── 📁 docs/                       # Documentation and guides
│   ├── 📁 prompts/                # User interaction logs with timestamps
│   ├── 📁 guides/                 # User guides and tutorials
│   └── 📁 architecture/           # Technical architecture documentation
│
├── 📄 main_simple.py              # FastAPI backend entry point
├── 📄 README.md                   # This documentation file
├── 📄 pyproject.toml              # Python project dependencies
└── 📄 uv.lock                     # Dependency lock file
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
- **Modern Bootstrap 5 UI**: Professional, responsive design with dark theme support
- **Real-time Progress Updates**: Visual feedback during document processing
- **Interactive Statistics**: Live processing metrics and performance analytics
- **Drag & Drop Upload**: Intuitive file upload with format validation
- **Multi-mode Processing**: Standard, Custom, and Multi-technique analysis modes
- **Solution Rationale**: Detailed explanations of confidence calculations and techniques used

### Core Functionality
- **Multi-Format Document Support**: PDF, DOCX, DOC, and Markdown (.md) files
- **Three Processing Modes**:
  - **Standard Fields**: Extract predefined common information
  - **Custom Fields**: User-specified comma-separated field extraction
  - **Multi-Technique Analysis**: Comparative analysis with 10 different extraction methods
- **Intelligent Document Classification**: Recognizes 3,700+ document varieties
- **Local NLP Processing**: No external API dependencies for data privacy
- **Advanced Pattern Recognition**: Enhanced regex and contextual matching
- **Real-time Processing**: Instant extraction with confidence scoring
- **Template Learning**: Ability to learn and recognize new document patterns

### Advanced Features (Phase 2)
- **Template Classification**: Recognizes 3,700+ document varieties across 10+ categories
- **State Compliance Detection**: Identifies requirements for all 50 US states
- **Enhanced Confidence Scoring**: Multi-algorithm validation with detailed confidence metrics
- **Organization Detection**: Identifies business entities and organizations
- **Document Complexity Analysis**: Assesses document structure and processing requirements
- **Template Learning**: Ability to learn and recognize new document patterns
- **Multi-technique Comparative Analysis**: Compare 10 different extraction methods with individual confidence scores

### Extraction Techniques
1. **Regex Pattern Matching** - Structured data identification
2. **Fuzzy String Matching** - Keyword proximity analysis  
3. **Keyword Proximity Analysis** - Distance-based value extraction
4. **Levenshtein Distance Matching** - Edit distance calculations
5. **Statistical Frequency Analysis** - Pattern frequency evaluation
6. **Context-Aware Extraction** - Semantic relationship mapping
7. **Template-Based Extraction** - Document structure recognition
8. **Position-Based Extraction** - Layout and position patterns
9. **Pattern Ensemble Method** - Combined technique approach
10. **Confidence-Weighted Extraction** - Machine learning enhanced

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+
- FastAPI
- Required Python packages (see Installation)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd nlp-document-extraction

# Install required dependencies
pip install django django-cors-headers fastapi uvicorn pdfplumber python-docx docx2txt python-multipart pydantic requests fuzzywuzzy python-levenshtein spacy joblib
```

### Run the Application

#### Method 1: Django Frontend + FastAPI Backend (Recommended)
```bash
# Terminal 1: Start the FastAPI backend
python main_simple.py

# Terminal 2: Start the Django frontend
python manage.py runserver 0.0.0.0:5000
```

#### Method 2: FastAPI Only (API Access)
```bash
python main_simple.py
```

### Access Points
- **Main Application**: `http://localhost:5000` - Django Dashboard (Use this for the web interface)
- **Backend API**: `http://localhost:8000` - FastAPI NLP processing engine (API only)
- **API Documentation**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Health Check**: `/api/health/` endpoint for monitoring both services

> **Important**: Always use `http://localhost:5000` for the web interface. The FastAPI backend at port 8000 is for API calls only.

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

### 1. Document Processor (`document_processor.py`)
- Multi-format text extraction (PDF, DOCX, DOC, MD)
- Document type classification
- Error handling for corrupted files

### 2. Simple Dynamic Extractor (`simple_extractor.py`)
- Pattern-based field extraction
- Fuzzy string matching
- Contextual analysis
- Custom field processing

### 3. Multi-Technique Extractor (`multi_technique_extractor_simple.py`)
- Comparative analysis across 10 techniques
- Individual confidence scoring
- Consolidated result generation
- Performance ranking

### 4. Template Classifier (`template_classifier.py`)
- Recognition of 3,700+ document varieties
- State-specific compliance detection
- Organization identification
- Template learning capabilities

### 5. Confidence Scorer (`confidence_scorer.py`)
- Multi-algorithm validation
- Quality grade assignment
- Risk factor assessment
- Detailed confidence metrics

### 6. Django Frontend (`dashboard/`)
- Modern Bootstrap 5 interface
- Real-time progress tracking
- Interactive result visualization
- Multi-mode processing support

## 📊 Usage Examples

### Standard Field Extraction
Upload a document and extract common fields like names, dates, addresses, phone numbers, and email addresses.

### Custom Field Extraction
Specify your own fields:
```
policy_number, issue_date, coverage_amount, premium, beneficiary_name
```

### Multi-Technique Analysis
Compare results from all 10 extraction techniques to find the most reliable method for your document type.

## 🔍 API Endpoints

### FastAPI Backend (`http://localhost:8000`)
- `POST /upload/` - Standard field extraction
- `POST /extract-custom/` - Custom field extraction
- `POST /multi-technique/` - Multi-technique analysis
- `POST /upload/advanced/` - Advanced processing with template recognition
- `GET /templates/` - List available templates
- `POST /templates/learn/` - Learn new templates
- `GET /state-requirements/{state}` - Get state-specific requirements
- `GET /health` - Basic health check
- `GET /docs` - API documentation

### Django Frontend (`http://localhost:5000`)
- `/` - Main dashboard interface
- `/upload/` - Document upload (proxied to FastAPI)
- `/extract-custom/` - Custom extraction (proxied to FastAPI)
- `/multi-technique/` - Multi-technique analysis (proxied to FastAPI)
- `/api/health/` - Combined health check

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

## 📈 Performance

- **Processing Speed**: 2-5 seconds per document (varies by size and complexity)
- **Memory Usage**: Optimized for documents up to 50MB
- **Concurrent Requests**: Supports multiple simultaneous uploads
- **Caching**: Template and pattern caching for improved performance

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

- **v2.0.0**: Django frontend integration, multi-technique analysis, advanced features
- **v1.0.0**: Initial FastAPI backend with basic extraction capabilities

---

**NLP Document Extraction Platform** - Intelligent document processing with advanced NLP capabilities.