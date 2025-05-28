# Real-Time Anomaly Detection System – Phase 1 (Local Setup)

This project sets up a real-time anomaly detection pipeline using Kafka, FastAPI, and a basic ML model. This README is focused on Phase 1: Local Development.

---

## 📁 Project Structure
```
anomaly-detector/
├── kafka-docker/                # Kafka + Zookeeper Docker Compose
├── fastapi-ml-service/          # FastAPI service serving the ML model
├── log-simulator/               # Generates simulated logs
├── processor/                   # Kafka consumer that calls ML API
└── README.md
```

---

## 🐳 Step 1: Kafka + Zookeeper Setup

1. Navigate to the `kafka-docker/` directory and create a `docker-compose.yml`:
```bash
version: '2'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

2. Start Kafka:
```bash
docker compose up -d
```

---

## 📝 Step 2: Simulate Logs

In `log-simulator/`, create `main.py`:
```python
import json, random, time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    log = {
        "timestamp": time.time(),
        "service": random.choice(["auth", "payment", "orders"]),
        "latency_ms": random.gauss(200, 50),
        "error_rate": random.random()
    }
    producer.send('logs', log)
    print("Sent:", log)
    time.sleep(1)
```
Install dependency:
```bash
pip install kafka-python
```

---

## ⚙️ Step 3: FastAPI ML Service

1. In `fastapi-ml-service/`, create `main.py`:
```python
from fastapi import FastAPI, Request
import joblib, numpy as np

app = FastAPI()
model = joblib.load("model.joblib")

@app.post("/predict")
async def predict(request: Request):
    payload = await request.json()
    features = np.array([[payload['latency_ms'], payload['error_rate']]])
    score = model.predict(features)[0]
    return {"anomaly": bool(score == -1)}
```

2. Train model:
```python
# save_model.py
from sklearn.ensemble import IsolationForest
import numpy as np, joblib

X_train = np.random.normal(200, 50, (1000, 2))
model = IsolationForest(contamination=0.05)
model.fit(X_train)
joblib.dump(model, "model.joblib")
```

Install:
```bash
pip install fastapi[all] scikit-learn joblib
uvicorn main:app --reload
```

---

## 🧾 Step 4: Kafka Consumer

In `processor/`, create `main.py`:
```python
import json, requests
from kafka import KafkaConsumer

consumer = KafkaConsumer('logs', bootstrap_servers='localhost:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

for message in consumer:
    log = message.value
    response = requests.post("http://localhost:8000/predict", json=log)
    print(f"Log: {log}, Anomaly: {response.json()['anomaly']}")
```

Install:
```bash
pip install kafka-python requests
```

---

## 🔁 Step 5: Run All Components

1. Start Kafka:
```bash
cd kafka-docker
docker compose up -d
```

2. Run simulator:
```bash
cd ../log-simulator
python main.py
```

3. Start FastAPI:
```bash
cd ../fastapi-ml-service
uvicorn main:app --reload
```

4. Run processor:
```bash
cd ../processor
python main.py
```

---

## ✅ Testing & Validation

- Use Kafka CLI to check logs:
```bash
docker exec -it <kafka_container> kafka-console-consumer   --bootstrap-server localhost:9092   --topic logs   --from-beginning
```

- Test FastAPI with curl:
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"latency_ms": 250, "error_rate": 0.4}'
```

---

## ✅ Requirements

- Python 3.8+
- Docker + Docker Compose
- pip: `kafka-python`, `fastapi`, `uvicorn`, `joblib`, `requests`, `scikit-learn`

---

## 📌 Next Step: EC2 Staging Deployment

Ensure end-to-end flow is stable and documented before deploying to AWS.
