# Real-Time Anomaly Detection System (AWS, Kafka, Flink, ML)

## Phase-wise Plan

---

## Use Cases

**Real-world applications of this anomaly detection system include:**

1. **Cloud Infrastructure Monitoring**
   - Detect unusual spikes in CPU, memory, network usage across services.
   - Proactively identify hardware or service failures.

2. **Fraud Detection in Fintech**
   - Monitor transaction logs in real-time for fraudulent behavior (e.g. abnormally high frequency, unusual IPs).

3. **Security and Intrusion Detection**
   - Identify suspicious login attempts, DDoS patterns, or unauthorized access in system logs.

4. **Microservices Health Monitoring**
   - Automatically detect failing microservices based on latency/error rate anomalies.
   - Route alerts to incident response teams.

5. **IoT Sensor Network Surveillance**
   - Detect faulty sensors by identifying outliers in streamed telemetry data.

6. **User Behavior Analytics**
   - Track real-time user interactions and identify behavioral anomalies that may indicate bot traffic or misuse.

7. **Retail and Inventory Management**
   - Detect abnormal sales or inventory drain patterns in retail systems.

---

## Phase 1: Development (Local Setup)

**Goal:** Build a functional pipeline locally to iterate quickly and validate the system.

### Week 1: Setup and Simulation (Elaborated)

1. **Project Structure Setup**
   ```bash
   mkdir -p anomaly-detector/{kafka-docker,fastapi-ml-service,log-simulator,processor}
   touch anomaly-detector/README.md
   ```

2. **Docker Compose Setup for Kafka + Zookeeper**
   In `kafka-docker/`, create a `docker-compose.yml`:
   ```yaml
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
   Run with:
   ```bash
   docker compose up -d
   ```

3. **Log Simulator**
   Create `log-simulator/main.py`:
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

4. **Validate Kafka Setup**
   List Docker containers:
   ```bash
   docker ps
   ```
   Find your Kafka container, then run:
   ```bash
   docker exec -it <kafka_container_name> kafka-console-consumer \
     --bootstrap-server localhost:9092 \
     --topic logs \
     --from-beginning
   ```

5. **README Documentation**
   - Document how to run Docker Compose
   - Document how to use the log simulator
   - List dependencies like `kafka-python`

**Tools:** Docker, Docker Compose, Python, kafka-python

**Time Estimate:** 1 week
