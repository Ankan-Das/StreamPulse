from fastapi import FastAPI, Request
import joblib
import numpy as np

from prometheus_client import start_http_server, Counter

REQUESTS = Counter("Total", "Total /predict requests")
ANOMALIES = Counter("Anomalies", "Anomalies predicted")

# Start Prometheus metrics server
start_http_server(8001)  # 👈 Starts a separate server at :8000/metrics

app = FastAPI()
model = joblib.load("model.joblib")     # Pre-trained Isolation Forest

@app.post("/predict")
async def predict(request: Request):
    REQUESTS.inc()
    
    payload = await request.json()
    features = np.array([[payload['latency_ms'], payload['error_rate']]])
    score = model.predict(features)[0]
    
    if score == -1:
        ANOMALIES.inc()
    
    return {"anomaly": bool(score == -1)}