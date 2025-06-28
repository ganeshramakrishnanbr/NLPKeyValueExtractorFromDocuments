import os
import json

# Mock processor since we don't have the actual LayoutLM dependencies installed
def process_document_with_layoutlm(image_path):
    """
    Process document with LayoutLM (mock version)
    """
    return {
        "success": True,
        "message": "Document processed successfully (simulated)",
        "file": os.path.basename(image_path),
        "mock_results": {
            "detected_layout": {
                "document_type": "invoice",
                "confidence": 0.92,
            },
            "extracted_entities": [
                {"text": "Invoice #12345", "type": "header", "box": [50, 50, 200, 80]},
                {"text": "Total: $1,234.56", "type": "amount", "box": [300, 400, 450, 430]},
                {"text": "Date: 12/31/2023", "type": "date", "box": [50, 100, 200, 120]}
            ]
        }
    }
