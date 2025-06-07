import json, random, time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092',
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