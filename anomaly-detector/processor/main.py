import json
import requests
from kafka import KafkaConsumer

consumer = KafkaConsumer('logs', bootstrap_servers='kafka:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))


for message in consumer:
    log = message.value
    response = requests.post("http://fastapi-ml-service:8000/predict", json=log)
    print(f"log: {log}, Anomaly: {response.json()}")