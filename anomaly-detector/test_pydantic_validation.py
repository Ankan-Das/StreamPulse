#!/usr/bin/env python3
"""
Test script to demonstrate Pydantic validation features in the anomaly detection API
"""

import requests
import json
from typing import Dict, Any

# API base URL (assuming service is running locally)
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints and validation features"""
    
    print("🧪 Testing Anomaly Detection API with Pydantic Validation")
    print("=" * 60)
    
    # Test 1: Service Info
    print("\n Testing Service Info Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service: {data['service']}")
            print(f"✅ Use Case: {data['use_case']}")
            print(f"✅ Features: {data['features']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Health Check
    print("\n Testing Health Check Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Use Case: {data['use_case']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Schema Endpoint
    print("\n Testing Schema Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/schema")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Use Case: {data['use_case']}")
            print(f"✅ Required Features: {data['required_features']}")
            print(f"✅ Example Payload: {json.dumps(data['example_payload'], indent=2)}")
            
            # Store example for later use
            example_payload = data['example_payload']
        else:
            print(f"❌ Failed: {response.status_code}")
            example_payload = {
                "trip_duration": 1800.0,
                "trip_distance": 5.2,
                "fare_amount": 15.50,
                "total_amount": 18.50
            }
    except Exception as e:
        print(f"❌ Error: {e}")
        example_payload = {
            "trip_duration": 1800.0,
            "trip_distance": 5.2,
            "fare_amount": 15.50,
            "total_amount": 18.50
        }
    
    # Test 4: Valid Prediction
    print("\n Testing Valid Prediction")
    try:
        response = requests.post(f"{BASE_URL}/predict", json=example_payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Anomaly: {data['anomaly']}")
            print(f"✅ Use Case: {data['use_case']}")
            print(f"✅ Features: {json.dumps(data['features'], indent=2)}")
            if data.get('confidence'):
                print(f"✅ Confidence: {data['confidence']:.3f}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Invalid Prediction - Missing Field
    print("\n Testing Invalid Prediction (Missing Field)")
    invalid_payload_1 = example_payload.copy()
    del invalid_payload_1['trip_duration']  # Remove required field
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=invalid_payload_1)
        if response.status_code == 422:  # Validation Error
            print("✅ Correctly rejected missing field")
            error_data = response.json()
            print(f"✅ Error details: {error_data['detail'][0]['msg']}")
        else:
            print(f"❌ Expected validation error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Invalid Prediction - Negative Value
    print("\n Testing Invalid Prediction (Negative Duration)")
    invalid_payload_2 = example_payload.copy()
    invalid_payload_2['trip_duration'] = -100.0  # Negative duration
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=invalid_payload_2)
        if response.status_code == 422:  # Validation Error
            print("✅ Correctly rejected negative duration")
            error_data = response.json()
            print(f"✅ Error details: {error_data['detail'][0]['msg']}")
        else:
            print(f"❌ Expected validation error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Invalid Prediction - Wrong Type
    print("\n Testing Invalid Prediction (Wrong Data Type)")
    invalid_payload_3 = example_payload.copy()
    invalid_payload_3['trip_distance'] = "not_a_number"  # String instead of number
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=invalid_payload_3)
        if response.status_code == 422:  # Validation Error
            print("✅ Correctly rejected wrong data type")
            error_data = response.json()
            print(f"✅ Error details: {error_data['detail'][0]['msg']}")
        else:
            print(f"❌ Expected validation error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 8: Edge Case - Zero Values
    print("\n Testing Edge Case (Zero Distance)")
    edge_payload = example_payload.copy()
    edge_payload['trip_distance'] = 0.0  # Zero distance should be allowed
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=edge_payload)
        if response.status_code == 200:
            print("✅ Correctly accepted zero distance")
            data = response.json()
            print(f"✅ Prediction completed: anomaly={data['anomaly']}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Pydantic validation tests completed!")
    print("📖 Check http://localhost:8000/docs for interactive API documentation")

if __name__ == "__main__":
    test_api_endpoints() 