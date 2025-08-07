import numpy as np

def extract_features(payload):
    """Extract features for NYC taxi use case"""
    return np.array([[
        payload['trip_duration'],
        payload['trip_distance'],
        payload['fare_amount'],
        payload['total_amount']
    ]])

def validate_payload(payload):
    """Validate incoming payload structure"""
    required_fields = ['trip_duration', 'trip_distance', 'fare_amount', 'total_amount']
    return all(field in payload for field in required_fields) 