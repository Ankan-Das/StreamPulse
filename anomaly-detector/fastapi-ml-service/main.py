import os
import yaml
import importlib.util
from fastapi import FastAPI, Request
import numpy as np
import joblib
from prometheus_client import start_http_server, Counter, Gauge

app = FastAPI()

# Load use case configuration
USE_CASE = os.getenv('USE_CASE', 'nyc_taxi')
config_path = f'/usecases/{USE_CASE}/config.yaml'

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Load model and scaler
model_path = f'/usecases/{USE_CASE}/{config["model"]["file"]}'
scaler_path = f'/usecases/{USE_CASE}/{config["model"]["scaler"]}'

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Load feature extraction module
features_module_path = f'/usecases/{USE_CASE}/features.py'
spec = importlib.util.spec_from_file_location("features", features_module_path)
features_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(features_module)

# Initialize metrics
prefix = config["metrics"]["prefix"]
TOTAL_MESSAGES = Counter(f'{prefix}_total_messages', "Total predict requests")
TOTAL_ANOMALIES = Counter(f'{prefix}_anomalies', "Anomalies predicted")

# Dynamic gauges based on config
gauges = {}
for feature in config["features"]:
    gauges[feature] = Gauge(f'{prefix}_latest_{feature}', f'Latest {feature}')

LATEST_IS_ANOMALY = Gauge(f'{prefix}_latest_is_anomaly', "Whether last message was anomaly")

# Start Prometheus metrics server
start_http_server(8001)

print(f"Started anomaly detection service for use case: {config['name']}")

@app.get("/")
async def root():
    return {
        "service": "Anomaly Detection API",
        "use_case": config["name"],
        "features": config["features"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "use_case": USE_CASE}

@app.post("/predict")
async def predict(request: Request):
    payload = await request.json()
    
    # Use dynamic feature extraction
    features = features_module.extract_features(payload)
    
    # Update metrics for each feature
    for i, feature_name in enumerate(config["features"]):
        if len(features[0]) > i:
            gauges[feature_name].set(features[0][i])
    
    # Make prediction
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    
    # Update counters
    TOTAL_MESSAGES.inc()
    is_anomaly = prediction == -1
    
    if is_anomaly:
        TOTAL_ANOMALIES.inc()
        LATEST_IS_ANOMALY.set(1)
        print(f"🚨 ANOMALY DETECTED for use case {USE_CASE}: {payload}")
    else:
        LATEST_IS_ANOMALY.set(0)
        print(f"✅ Normal prediction for use case {USE_CASE}")
    
    return {
        "anomaly": bool(is_anomaly),
        "use_case": USE_CASE,
        "features": dict(zip(config["features"], [float(f) for f in features[0]]))
    }