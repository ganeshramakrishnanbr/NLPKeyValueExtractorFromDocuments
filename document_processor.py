import pdfplumber
import docx
import docx2txt
from typing import Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Document processor for extracting text from various file formats
    and performing basic document classification.
    """
    
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'doc']
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from PDF, DOCX, or DOC files
        
        Args:
            file_path: Path to the document file
            file_type: Type of file (pdf, docx, doc)
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If file type is not supported
            Exception: If text extraction fails
        """
        file_type = file_type.lower()
        
        if file_type not in self.supported_formats:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        try:
            if file_type == 'pdf':
                return self._extract_pdf_text(file_path)
            elif file_type == 'docx':
                return self._extract_docx_text(file_path)
            elif file_type == 'doc':
                return self._extract_doc_text(file_path)
        except Exception as e:
            logger.error(f"Error extracting text from {file_type} file: {str(e)}")
            raise Exception(f"Failed to extract text from {file_type} file: {str(e)}")
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF using pdfplumber"""
        text_content = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content.append(page_text)
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                        continue
            
            extracted_text = '\n\n'.join(text_content)
            logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF")
            return extracted_text
            
        except Exception as e:
            raise Exception(f"PDF processing error: {str(e)}")
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX using python-docx"""
        try:
            doc = docx.Document(file_path)
            text_content = []
            
            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_content.append(' | '.join(row_text))
            
            extracted_text = '\n'.join(text_content)
            logger.info(f"Successfully extracted {len(extracted_text)} characters from DOCX")
            return extracted_text
            
        except Exception as e:
            raise Exception(f"DOCX processing error: {str(e)}")
        
    def _extract_doc_text(self, file_path: str) -> str:
        """Extract text from legacy DOC files using docx2txt"""
        try:
            extracted_text = docx2txt.process(file_path)
            if not extracted_text:
                raise Exception("No text could be extracted from DOC file")
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters from DOC")
            return extracted_text
            
        except Exception as e:
            raise Exception(f"DOC processing error: {str(e)}")
    
    def classify_document_type(self, text: str) -> str:
        """
        Basic document type classification using keyword matching
        
        Args:
            text: Extracted text from document
            
        Returns:
            Document type classification
        """
        # Document type keywords
        keywords = {
            "employment_document": [
                "employment", "employee", "employment contract", "job offer", "work agreement",
                "salary", "wage", "position", "department", "employer", "hire", "staff"
            ],
            "financial_document": [
                "bank statement", "financial", "account", "balance", "transaction",
                "deposit", "withdrawal", "investment", "loan", "credit", "debit"
            ],
            "legal_document": [
                "contract", "agreement", "legal", "terms", "conditions", "clause",
                "party", "witness", "notary", "court", "jurisdiction"
            ],
            "medical_document": [
                "medical", "health", "patient", "doctor", "physician", "treatment",
                "diagnosis", "prescription", "hospital", "clinic", "healthcare"
            ],
            "insurance_document": [
                "insurance", "policy", "coverage", "premium", "deductible", "claim",
                "beneficiary", "insured", "insurer", "protection"
            ],
            "educational_document": [
                "education", "school", "university", "student", "course", "grade",
                "transcript", "diploma", "certificate", "academic"
            ],
            "identification_document": [
                "identification", "id", "passport", "license", "permit", "certificate",
                "registration", "official", "government", "issued"
            ]
        }
        
        text_lower = text.lower()
        
        # Count keyword matches for each document type
        type_scores = {}
        for doc_type, keyword_list in keywords.items():
            score = sum(1 for keyword in keyword_list if keyword in text_lower)
            if score > 0:
                type_scores[doc_type] = score
        
        # Return the document type with the highest score
        if type_scores:
            best_match = max(type_scores, key=type_scores.get)
            logger.info(f"Document classified as: {best_match} (score: {type_scores[best_match]})")
            return best_match
        
        # Default to unknown if no keywords match
        logger.info("Document type could not be determined - classified as unknown")
        return "unknown"
