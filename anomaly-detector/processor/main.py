import os
import yaml
import json
import requests
from kafka import KafkaConsumer
from prometheus_client import start_http_server, Counter

# Load use case configuration
USE_CASE = os.getenv('USE_CASE', 'nyc_taxi')
config_path = f'/usecases/{USE_CASE}/config.yaml'

try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise Exception(f"Configuration file not found for use case: {USE_CASE}")

# Initialize metrics with dynamic naming
prefix = config["metrics"]["prefix"]
MESSAGES = Counter(f'{prefix}_processor_messages', "Messages received from Kafka")
ANOMALIES = Counter(f'{prefix}_processor_anomalies', "Anomalies detected")

# Start Prometheus metrics server
start_http_server(9000)

print(f"Started processor for use case: {config['name']}")
print(f"Kafka topic: {config['kafka']['topic']}")
print(f"Consumer group: {config['kafka']['consumer_group']}")

# Initialize Kafka consumer with dynamic configuration
consumer = KafkaConsumer(
    config["kafka"]["topic"],
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP', 'kafka:9092'),
    group_id=config["kafka"]["consumer_group"],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True
)

print(f"Processor ready - listening for messages on topic: {config['kafka']['topic']}")

for message in consumer:
    try:
        log = message.value
        MESSAGES.inc()
        
        # Send to FastAPI ML service for prediction
        response = requests.post(
            "http://fastapi-ml-service:8000/predict", 
            json=log,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("anomaly"):
                ANOMALIES.inc()
                print(f"🚨 ANOMALY DETECTED - Use case: {USE_CASE}, Data: {log}, Response: {result}")
            else:
                print(f"✅ Normal - Use case: {USE_CASE}, Data: {log}")
        else:
            print(f"❌ Error from ML service: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error processing message: {e}")