from fastapi import FastAPI, Request
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model.joblib")     # Pre-trained Isolation Forest

@app.post("/predict")
async def predict(request: Request):
    payload = await request.json()
    features = np.array([[payload['latency_ms'], payload['error_rate']]])
    score = model.predict(features)[0]
    return {"anomaly": bool(score == -1)}