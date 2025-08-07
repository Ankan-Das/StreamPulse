# Multi-Use Case Anomaly Detection System

This system now supports multiple use cases for anomaly detection with a simple environment variable configuration.

## Current Structure

```
anomaly-detector/
├── usecases/
│   └── nyc_taxi/
│       ├── config.yaml          # Use case configuration
│       ├── model_taxi.joblib    # Trained model
│       ├── scaler_taxi.joblib   # Feature scaler
│       ├── features.py          # Feature extraction logic
│       └── stream_simulator.py  # Data simulator
├── fastapi-ml-service/          # Dynamic ML service
├── processor/                   # Dynamic processor
└── docker-compose.yml          # Updated with USE_CASE support
```

## Usage

### Running Different Use Cases

```bash
# Run NYC taxi use case (default)
USE_CASE=nyc_taxi docker-compose up

# When you add more use cases:
# USE_CASE=web_logs docker-compose up
# USE_CASE=network_traffic docker-compose up
```

### Testing the Current Setup

1. **Start the system:**
   ```bash
   USE_CASE=nyc_taxi docker-compose up
   ```

2. **Check service status:**
   ```bash
   curl http://localhost:8000/
   curl http://localhost:8000/health
   ```

3. **Access monitoring:**
   - Grafana: http://localhost:3000
   - Prometheus: http://localhost:9090
   - FastAPI docs: http://localhost:8000/docs

## Adding New Use Cases

To add a new use case (e.g., `web_logs`):

### 1. Create Use Case Directory
```bash
mkdir usecases/web_logs
```

### 2. Create Configuration File
Create `usecases/web_logs/config.yaml`:
```yaml
name: "web_logs"
description: "Web Log Anomaly Detection"
kafka:
  topic: "web-logs"
  consumer_group: "web-logs-processor"
model:
  file: "model.joblib"
  scaler: "scaler.joblib"
features:
  - response_time
  - request_size
  - status_code
  - user_agent_entropy
metrics:
  prefix: "web_logs"
  labels:
    - response_time
    - request_size
    - status_code
    - user_agent_entropy
```

### 3. Create Features Module
Create `usecases/web_logs/features.py`:
```python
import numpy as np

def extract_features(payload):
    """Extract features for web logs use case"""
    return np.array([[
        payload['response_time'],
        payload['request_size'],
        payload['status_code'],
        payload['user_agent_entropy']
    ]])

def validate_payload(payload):
    """Validate incoming payload structure"""
    required_fields = ['response_time', 'request_size', 'status_code', 'user_agent_entropy']
    return all(field in payload for field in required_fields)
```

### 4. Add Model Files
- Train your model and save as `usecases/web_logs/model.joblib`
- Save your scaler as `usecases/web_logs/scaler.joblib`

### 5. Create Data Simulator
Create `usecases/web_logs/stream_simulator.py` to generate test data.

### 6. Add Dockerfile
Create `usecases/web_logs/Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "stream_simulator.py"]
```

### 7. Run the New Use Case
```bash
USE_CASE=web_logs docker-compose up
```

## Configuration Details

### config.yaml Fields

- **name**: Human-readable name for the use case
- **description**: Brief description of what this use case detects
- **kafka.topic**: Kafka topic name for this use case
- **kafka.consumer_group**: Consumer group for the processor
- **model.file**: Filename of the trained model
- **model.scaler**: Filename of the feature scaler
- **features**: List of feature names (order matters!)
- **metrics.prefix**: Prefix for Prometheus metrics
- **metrics.labels**: Labels for Grafana dashboards

### Features Module Requirements

Each `features.py` must implement:
- `extract_features(payload)`: Returns numpy array of features
- `validate_payload(payload)`: Returns boolean for payload validation

## Monitoring

The system automatically creates dynamic Prometheus metrics based on your configuration:
- `{prefix}_total_messages`: Total prediction requests
- `{prefix}_anomalies`: Total anomalies detected
- `{prefix}_latest_{feature}`: Latest value for each feature
- `{prefix}_latest_is_anomaly`: Latest anomaly status

## API Endpoints

- `GET /`: Service information and current use case
- `GET /health`: Health check
- `POST /predict`: Make predictions (accepts use-case specific payload)
- `GET /docs`: Interactive API documentation

## Environment Variables

- `USE_CASE`: Selects which use case to run (default: `nyc_taxi`)
- `KAFKA_BOOTSTRAP`: Kafka bootstrap servers (default: `kafka:9092`)

## Benefits

1. **Easy switching**: Change use cases with one environment variable
2. **Consistent structure**: All use cases follow the same pattern
3. **Dynamic metrics**: Prometheus metrics adapt to each use case
4. **Modular design**: Each use case is self-contained
5. **Scalable**: Easy to add new use cases without changing core services 