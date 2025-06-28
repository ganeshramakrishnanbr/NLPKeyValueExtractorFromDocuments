"""
Standalone NLP Document Key-Value Extractor

This script provides the core functionality without requiring server setup.
It can process documents directly from the filesystem.
"""
import os
import sys
import re
import json
from pathlib import Path
import time

def extract_key_value_pairs(text):
    """Extract key-value pairs from text using regex patterns"""
    patterns = {
        'name': r'(?:name|Name)[:\s]+([A-Za-z\s.-]+)',
        'ssn': r'(?:ss[n#]|SSN)[:\s]+(\d{3}[-\s]?\d{2}[-\s]?\d{4})',
        'date_of_birth': r'(?:date\s+of\s+birth|dob|born|Date\s+of\s+Birth|DOB)[:\s]+((\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4})|([A-Za-z]+\s+\d{1,2}[,\s]+\d{4}))',
        'phone': r'(?:phone|tel|telephone|mobile|Phone)[:\s]*(\+?[\d\s.-]{10,})',
        'email': r'(?:email|Email)[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        'address': r'(?:address|addr|Address)[:\s]+([A-Za-z0-9\s.,#-]+)',
        'policy_number': r'(?:policy|policy\s+number|policy\s+#|Policy\s+Number)[:\s]+([A-Za-z0-9-]+)',
        'policy_type': r'(?:policy\s+type|insurance\s+type|Policy\s+Type)[:\s]+([A-Za-z\s]+)',
        'coverage_amount': r'(?:coverage|coverage\s+amount|Coverage\s+Amount)[:\s]+(\$[\d,]+)',
        'premium': r'(?:premium|Premium)[:\s]+([\$\d,.]+(?:\/[a-z]+)?)',
    }
    
    # Additional patterns for markdown-style formatting
    md_patterns = {
        'name': r'\*\*(?:Name|name):\*\*\s+([A-Za-z\s.-]+)',
        'ssn': r'\*\*(?:SSN|ssn):\*\*\s+(\d{3}[-\s]?\d{2}[-\s]?\d{4})',
        'date_of_birth': r'\*\*(?:Date\s+of\s+Birth|DOB):\*\*\s+((\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4})|([A-Za-z]+\s+\d{1,2}[,\s]+\d{4}))',
        'phone': r'\*\*(?:Phone|phone):\*\*\s+(\+?[\d\s.-]{10,})',
        'email': r'\*\*(?:Email|email):\*\*\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        'address': r'\*\*(?:Address|address):\*\*\s+([A-Za-z0-9\s.,#-]+)',
        'policy_number': r'\*\*(?:Policy\s+Number|policy):\*\*\s+([A-Za-z0-9-]+)',
        'policy_type': r'\*\*(?:Policy\s+Type|policy\s+type):\*\*\s+([A-Za-z\s]+)',
        'coverage_amount': r'\*\*(?:Coverage\s+Amount|coverage):\*\*\s+(\$[\d,]+)',
        'premium': r'\*\*(?:Premium|premium):\*\*\s+([\$\d,.]+(?:\/[a-z]+)?)',
    }
    
    results = {}
    
    # Process using standard patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Get the value part (usually in group 1 or 2)
            value = match.group(1) if len(match.groups()) > 0 else match.group(0)
            results[key] = value.strip()
    
    # Process using markdown patterns
    for key, pattern in md_patterns.items():
        match = re.search(pattern, text)
        if match and key not in results:  # Only add if not already found
            value = match.group(1) if len(match.groups()) > 0 else match.group(0)
            results[key] = value.strip()
    
    return results

def extract_from_file(file_path):
    """Process a file and extract key-value pairs"""
    start_time = time.time()
    
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    # Get file extension
    ext = Path(file_path).suffix.lower()
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}
    
    # Extract key-value pairs
    extracted_data = extract_key_value_pairs(text)
    
    # Calculate confidence score based on number of fields found
    total_fields = len(extracted_data)
    possible_fields = 10  # Total number of fields we're looking for
    confidence_score = min(1.0, total_fields / possible_fields)
    
    # Format results
    result = {
        "filename": os.path.basename(file_path),
        "file_type": ext,
        "file_size": os.path.getsize(file_path),
        "extracted_fields": extracted_data,
        "confidence_score": confidence_score,
        "processing_time": round(time.time() - start_time, 2)
    }
    
    return result

if __name__ == "__main__":
    # Check if file path is provided
    if len(sys.argv) < 2:
        print("Usage: python standalone_extractor.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = extract_from_file(file_path)
    
    # Print result as formatted JSON
    print(json.dumps(result, indent=2))
