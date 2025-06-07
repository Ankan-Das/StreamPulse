import json
import requests
from kafka import KafkaConsumer

from prometheus_client import start_http_server, Counter

MESSAGES = Counter("processor_messages", "Messages received from Kafka")
ANOMALIES = Counter("processor_anomalies", "Anomalies detected")

start_http_server(9000)

consumer = KafkaConsumer('logs', bootstrap_servers='kafka:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))


for message in consumer:
    log = message.value
    response = requests.post("http://fastapi-ml-service:8000/predict", json=log)
    print(f"log: {log}, Anomaly: {response.json()}")