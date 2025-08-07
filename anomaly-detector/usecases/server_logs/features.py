import numpy as np
from datetime import datetime
import re

def extract_features(payload):
    """Extract features for server logs use case"""
    return np.array([[
        payload['response_time'],
        payload['request_size'],
        payload['status_code_numeric'],
        payload['hour_of_day'],
        payload['requests_per_minute']
    ]])

def validate_payload(payload):
    """Validate incoming payload structure"""
    required_fields = [
        'response_time', 
        'request_size', 
        'status_code_numeric', 
        'hour_of_day', 
        'requests_per_minute'
    ]
    return all(field in payload for field in required_fields)

def parse_apache_log(log_line):
    """Parse Apache log line and extract features
    
    Expected format: Combined Log Format
    IP - - [timestamp] "method path protocol" status size "referer" "user-agent"
    """
    # Apache Combined Log Format regex
    pattern = r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) (\S+)" (\d+) (\d+|-) "(.*?)" "(.*?)"'
    
    match = re.match(pattern, log_line)
    if not match:
        return None
    
    ip, timestamp, method, path, protocol, status, size, referer, user_agent = match.groups()
    
    # Parse timestamp
    try:
        dt = datetime.strptime(timestamp.split()[0], '%d/%b/%Y:%H:%M:%S')
        hour_of_day = dt.hour
    except:
        hour_of_day = 0
    
    # Extract features
    try:
        status_code = int(status)
        request_size = int(size) if size != '-' else 0
        
        # Calculate response time (simulated based on request size and status)
        if status_code >= 400:
            response_time = np.random.uniform(1000, 5000)  # Error responses take longer
        elif request_size > 10000:
            response_time = np.random.uniform(500, 2000)   # Large requests take longer
        else:
            response_time = np.random.uniform(100, 800)    # Normal responses
        
        # Simulate requests per minute (this would normally come from aggregation)
        requests_per_minute = np.random.uniform(10, 100)
        
        return {
            'ip': ip,
            'timestamp': timestamp,
            'method': method,
            'path': path,
            'status_code': status_code,
            'status_code_numeric': float(status_code),
            'request_size': float(request_size),
            'response_time': response_time,
            'hour_of_day': float(hour_of_day),
            'requests_per_minute': requests_per_minute,
            'user_agent': user_agent
        }
    except Exception as e:
        print(f"Error parsing log line: {e}")
        return None 