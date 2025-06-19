#!/usr/bin/env python3
"""
Test script to verify Markdown file processing functionality
"""

import requests
import json
from pathlib import Path

def test_markdown_processing():
    """Test the Markdown file processing with sample data"""
    
    # API endpoint
    base_url = "http://localhost:8000"
    
    # Test file
    test_file = "sample_test.md"
    
    if not Path(test_file).exists():
        print(f"❌ Test file {test_file} not found")
        return False
    
    print("🧪 Testing Markdown File Processing")
    print("=" * 50)
    
    # Test 1: Standard extraction
    print("\n1. Testing Standard Field Extraction...")
    try:
        with open(test_file, 'rb') as file:
            files = {'file': (test_file, file, 'text/markdown')}
            response = requests.post(f"{base_url}/upload/", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Standard extraction successful")
            print(f"   Document type: {result['document_type']}")
            print(f"   Confidence: {result['confidence_score']:.2f}")
            print(f"   Processing time: {result['processing_time']:.2f}s")
            
            # Show extracted customer info
            customer = result['customer_info']
            if customer['name']:
                print(f"   Name: {customer['name']}")
            if customer['email']:
                print(f"   Email: {customer['email']}")
            if customer['phone']:
                print(f"   Phone: {customer['phone']}")
        else:
            print(f"❌ Standard extraction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Standard extraction error: {str(e)}")
        return False
    
    # Test 2: Custom field extraction
    print("\n2. Testing Custom Field Extraction...")
    try:
        custom_fields = "name,email,phone,employee_id,salary,department,manager"
        
        with open(test_file, 'rb') as file:
            files = {'file': (test_file, file, 'text/markdown')}
            data = {'fields': custom_fields}
            response = requests.post(f"{base_url}/extract-custom/", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Custom extraction successful")
            print(f"   Document type: {result['document_type']}")
            print(f"   Confidence: {result['confidence_score']:.2f}")
            print(f"   Fields requested: {len(result['requested_fields'])}")
            print(f"   Fields extracted: {len([v for v in result['extracted_fields'].values() if v])}")
            
            # Show extracted custom fields
            for field, value in result['extracted_fields'].items():
                if value:
                    print(f"   {field}: {value}")
        else:
            print(f"❌ Custom extraction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Custom extraction error: {str(e)}")
        return False
    
    print("\n🎉 All Markdown processing tests passed!")
    return True

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🔍 Markdown File Processing Test Suite")
    print("=" * 50)
    
    # Check if API is running
    if not test_api_health():
        print("❌ API is not running. Please start the server first:")
        print("   python main_simple.py")
        exit(1)
    
    print("✅ API is running")
    
    # Run tests
    success = test_markdown_processing()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("Markdown file support is working correctly.")
    else:
        print("\n❌ Some tests failed.")
        exit(1)