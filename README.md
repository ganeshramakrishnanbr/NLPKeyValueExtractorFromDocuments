# NLP Key Value Extractor From Documents

A powerful Python application that extracts key-value information from any document type using intelligent pattern recognition and NLP techniques.

## Features

- **Document Support**: PDF, DOCX, DOC, and Markdown (.md) file formats
- **Dual Processing Modes**:
  - **Standard Fields**: Extract common information (name, email, phone, address, etc.)
  - **Custom Fields**: Specify any fields you need extracted
- **Document Classification**: Automatically categorizes documents into 7 types
- **Web Interface**: Clean, responsive UI with drag-and-drop upload
- **REST API**: Complete API with interactive documentation
- **Confidence Scoring**: Measures extraction accuracy

## Quick Start

### Installation
```bash
pip install fastapi uvicorn pdfplumber python-docx docx2txt
```

### Run the Application
```bash
python main_simple.py
```

Access the web interface at `http://localhost:8000`

## Git Automation

This repository includes automated git commit tools for efficient development workflow. The automation system is fully tested and working in Replit environment.

### Available Commands

```bash
# Full auto-commit with custom message
./autocommit.sh "Add new feature"

# Auto-commit with timestamp
./autocommit.sh

# Quick commit (shorter script)
./quick-commit.sh "Fix bug in extraction"

# Git aliases (after setup)
git ac "Your message"     # Auto-commit
git qc "Your message"     # Quick commit with confirmation
git acp                   # Auto-commit with timestamp
```

### Setup Git Automation
```bash
./setup-git-automation.sh
```

This creates git aliases and makes all scripts executable.

## API Usage

### Standard Extraction
```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Custom Field Extraction
```bash
curl -X POST "http://localhost:8000/extract-custom/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "fields=name,email,employee_id,salary"
```

### Markdown File Processing
```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@README.md"
```

## Project Structure

```
├── main_simple.py          # Main FastAPI application
├── models.py               # Pydantic data models
├── document_processor.py   # Document text extraction
├── simple_extractor.py     # Pattern-based field extraction
├── templates/index.html    # Web interface
├── autocommit.sh          # Git automation script
├── quick-commit.sh        # Quick git commit
└── setup-git-automation.sh # Setup script
```

## Document Types Supported

The system automatically classifies documents into:
- Employment documents
- Financial documents  
- Legal documents
- Medical documents
- Insurance documents
- Educational documents
- Identification documents

## Custom Field Examples

Extract any fields by specifying them in Custom Fields mode:

**HR Documents**: `employee_id, department, salary, start_date, manager`
**Financial Records**: `account_number, balance, transaction_date, amount`
**Legal Contracts**: `contract_number, party_1, party_2, effective_date, terms`
**Medical Records**: `patient_id, diagnosis, treatment, doctor, visit_date`

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Use the git automation tools for consistent commits:

```bash
# Make changes
./autocommit.sh "Implement new extraction algorithm"

# Or use quick commit
git qc "Fix extraction bug"
```