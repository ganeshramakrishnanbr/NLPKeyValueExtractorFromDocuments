#!/usr/bin/env python3
"""
Test script to verify custom field extraction returns exactly requested fields
"""

import requests
import json
from pathlib import Path

def test_custom_field_matching():
    """Test that custom extraction returns exactly the requested fields"""
    
    base_url = "http://localhost:8000"
    test_file = "sample_test.md"
    
    if not Path(test_file).exists():
        print("Test file not found")
        return False
    
    print("Testing Custom Field Exact Matching")
    print("=" * 50)
    
    # Test different field combinations
    test_cases = [
        {
            "name": "Basic Employee Fields", 
            "fields": "name,email,phone,employee_id"
        },
        {
            "name": "Financial Fields",
            "fields": "salary,department,manager,start_date"
        },
        {
            "name": "Mixed Custom Fields",
            "fields": "position,company,benefits,vacation_days"
        },
        {
            "name": "Single Field",
            "fields": "name"
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Requested: {test_case['fields']}")
        
        try:
            with open(test_file, 'rb') as file:
                files = {'file': (test_file, file, 'text/markdown')}
                data = {'fields': test_case['fields']}
                response = requests.post(f"{base_url}/extract-custom/", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                requested_fields = test_case['fields'].split(',')
                requested_fields = [f.strip() for f in requested_fields]
                returned_fields = list(result['extracted_fields'].keys())
                
                print(f"Requested fields: {requested_fields}")
                print(f"Returned fields: {returned_fields}")
                
                # Check if returned fields match exactly
                if set(requested_fields) == set(returned_fields):
                    print("✅ Perfect match - returned exactly requested fields")
                else:
                    print("❌ Mismatch detected")
                    missing = set(requested_fields) - set(returned_fields)
                    extra = set(returned_fields) - set(requested_fields)
                    if missing:
                        print(f"   Missing: {missing}")
                    if extra:
                        print(f"   Extra: {extra}")
                
                # Show extracted values
                found_values = {k: v for k, v in result['extracted_fields'].items() if v}
                print(f"Values found: {len(found_values)}/{len(requested_fields)}")
                for field, value in found_values.items():
                    print(f"   {field}: {value}")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    return True

if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("API is not running. Start with: python main_simple.py")
            exit(1)
    except:
        print("API is not running. Start with: python main_simple.py")
        exit(1)
    
    test_custom_field_matching()