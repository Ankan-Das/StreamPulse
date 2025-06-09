from fastapi import FastAPI, Request
import numpy as np
import joblib

app = FastAPI()

# Load model and scaler
model = joblib.load('model_taxi.joblib')
scaler = joblib.load('scaler_taxi.joblib')

# Prometheus metrics
from prometheus_client import start_http_server, Counter, Gauge
TOTAL_MESSAGES = Counter("Total", "Total /predict requests")
TOTAL_ANOMALIES = Counter("Anomalies", "Anomalies predicted")

# Gauge metrics — overwrite each time a log is processed
LATEST_TRIP_DURATION = Gauge("latest_trip_duration", "Trip duration of last processed message")
LATEST_TRIP_DISTANCE = Gauge("latest_trip_distance", "Trip distance of last processed message")
LATEST_FARE_AMOUNT = Gauge("latest_fare_amount", "Fare amount of last processed message")
LATEST_TOTAL_AMOUNT = Gauge("latest_total_amount", "Total amount of last processed message")
LATEST_IS_ANOMALY = Gauge("latest_is_anomaly", "Whether last message was anomaly (1=True, 0=False)")

# Start Prometheus metrics server
start_http_server(8001)  # 👈 Starts a separate server at :8000/metrics

@app.post("/predict")
async def predict(request: Request):
    
    payload = await request.json()
    
    features = np.array([[
        payload['trip_duration'],
        payload['trip_distance'],
        payload['fare_amount'],
        payload['total_amount']
    ]])
    
    LATEST_TRIP_DURATION.set(payload["trip_duration"]/100)
    LATEST_TRIP_DISTANCE.set(payload["trip_distance"])
    LATEST_FARE_AMOUNT.set(payload["fare_amount"])
    LATEST_TOTAL_AMOUNT.set(payload["total_amount"])

    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    
    TOTAL_MESSAGES.inc()
    if prediction == -1:
        TOTAL_ANOMALIES.inc()
        LATEST_IS_ANOMALY.set(80)
        print("ANOMALY FOOUnd")
    else:
        LATEST_IS_ANOMALY.set(-10)
    
    return {"anomaly": bool(prediction == -1)}