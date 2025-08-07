#!/usr/bin/env python3
"""
🖥️ Server Logs Stream Simulator

This simulator generates realistic server log events and sends them to Kafka
for real-time anomaly detection.

Features:
- Realistic server log patterns (response times, status codes, request sizes)
- Time-based patterns (peak hours, off-hours)
- Configurable anomaly injection
- Apache-style log parsing
"""

import json
import time
import random
import numpy as np
from datetime import datetime, timedelta
from kafka import KafkaProducer
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServerLogsSimulator:
    def __init__(self, kafka_bootstrap='kafka:9092', topic='server-logs'):
        self.kafka_bootstrap = kafka_bootstrap
        self.topic = topic
        self.producer = None
        self.running = False
        
        # Server log generation parameters
        self.base_requests_per_minute = 60
        self.anomaly_probability = 0.05  # 5% chance of anomaly
        
        # Initialize Kafka producer
        self._init_kafka_producer()
        
    def _init_kafka_producer(self):
        """Initialize Kafka producer with retry logic"""
        max_retries = 10
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=self.kafka_bootstrap,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    retry_backoff_ms=1000,
                    request_timeout_ms=30000,
                    api_version=(0, 10, 1)
                )
                logger.info(f"✅ Connected to Kafka at {self.kafka_bootstrap}")
                return
            except Exception as e:
                logger.error(f"❌ Failed to connect to Kafka (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    logger.info(f"⏳ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"Failed to connect to Kafka after {max_retries} attempts")
    
    def get_current_hour_stats(self):
        """Get realistic traffic patterns based on current hour"""
        current_hour = datetime.now().hour
        
        # Define traffic patterns (multiplier of base rate)
        if 9 <= current_hour <= 17:  # Business hours
            traffic_multiplier = random.uniform(1.5, 3.0)
            error_rate = 0.02  # 2% error rate during business hours
        elif 18 <= current_hour <= 22:  # Evening
            traffic_multiplier = random.uniform(0.8, 1.5)
            error_rate = 0.03  # 3% error rate
        elif 23 <= current_hour or current_hour <= 6:  # Night
            traffic_multiplier = random.uniform(0.2, 0.6)
            error_rate = 0.01  # 1% error rate (mostly automated traffic)
        else:  # Early morning/late evening
            traffic_multiplier = random.uniform(0.6, 1.2)
            error_rate = 0.025  # 2.5% error rate
            
        return traffic_multiplier, error_rate
    
    def generate_normal_log_entry(self):
        """Generate a normal server log entry"""
        current_time = datetime.now()
        traffic_multiplier, error_rate = self.get_current_hour_stats()
        
        # Generate request characteristics
        method = random.choice(['GET'] * 70 + ['POST'] * 20 + ['PUT'] * 5 + ['DELETE'] * 3 + ['HEAD'] * 2)
        
        # Status codes based on method and error rate
        if random.random() < error_rate:
            status_code = random.choice([400, 404, 500, 502, 503])
        else:
            if method == 'GET':
                status_code = random.choice([200] * 80 + [304] * 20)
            else:
                status_code = random.choice([200] * 85 + [201] * 10 + [204] * 5)
        
        # Request size based on method
        if method == 'GET':
            request_size = random.lognormal(6, 1)  # Smaller requests
        elif method == 'POST':
            request_size = random.lognormal(8, 1.5)  # Larger requests
        else:
            request_size = random.lognormal(7, 1.2)  # Medium requests
        
        # Response time based on status code and request size
        if status_code >= 500:  # Server errors
            response_time = random.gamma(3, 800)  # Slower due to errors
        elif status_code >= 400:  # Client errors
            response_time = random.gamma(2, 200)  # Fast error responses
        elif status_code == 304:  # Not modified
            response_time = random.gamma(1, 50)   # Very fast
        else:  # Success
            base_time = 150 + (request_size / 1000) * 10  # Larger requests take longer
            response_time = random.gamma(2, base_time / 2)
        
        # Calculate requests per minute based on traffic pattern
        requests_per_minute = self.base_requests_per_minute * traffic_multiplier + random.normal(0, 10)
        
        return {
            'timestamp': current_time.isoformat(),
            'method': method,
            'status_code': status_code,
            'status_code_numeric': float(status_code),
            'request_size': max(100, request_size),  # Minimum 100 bytes
            'response_time': max(50, response_time),  # Minimum 50ms
            'hour_of_day': float(current_time.hour),
            'requests_per_minute': max(1, requests_per_minute),
            'ip': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'path': random.choice([
                '/', '/api/users', '/api/data', '/login', '/dashboard',
                '/static/css/style.css', '/static/js/app.js', '/favicon.ico',
                '/api/status', '/health', '/metrics'
            ]),
            'user_agent': random.choice([
                'Mozilla/5.0 (Chrome)', 'Mozilla/5.0 (Firefox)', 
                'Mozilla/5.0 (Safari)', 'curl/7.68.0', 'Python-requests'
            ])
        }
    
    def generate_anomaly_log_entry(self):
        """Generate an anomalous server log entry"""
        current_time = datetime.now()
        
        # Choose type of anomaly
        anomaly_types = [
            'ddos_attack',     # High traffic, slow responses
            'error_spike',     # Many error status codes
            'large_request',   # Unusually large requests
            'slow_response',   # Very slow response times
            'night_activity',  # Unusual activity at night
            'scan_attack'      # Systematic scanning patterns
        ]
        
        anomaly_type = random.choice(anomaly_types)
        
        if anomaly_type == 'ddos_attack':
            # DDoS attack simulation
            return {
                'timestamp': current_time.isoformat(),
                'method': 'GET',
                'status_code': random.choice([200, 503, 504]),
                'status_code_numeric': float(random.choice([200, 503, 504])),
                'request_size': random.uniform(500, 2000),
                'response_time': random.uniform(5000, 15000),  # Very slow
                'hour_of_day': float(current_time.hour),
                'requests_per_minute': random.uniform(300, 500),  # High traffic
                'ip': f"10.0.{random.randint(1, 10)}.{random.randint(1, 255)}",  # Suspicious IP range
                'path': '/',
                'user_agent': 'AttackBot/1.0'
            }
        
        elif anomaly_type == 'error_spike':
            # Error spike simulation
            return {
                'timestamp': current_time.isoformat(),
                'method': random.choice(['POST', 'PUT', 'DELETE']),
                'status_code': random.choice([500, 502, 503, 404, 403]),
                'status_code_numeric': float(random.choice([500, 502, 503, 404, 403])),
                'request_size': random.uniform(1000, 5000),
                'response_time': random.uniform(2000, 8000),
                'hour_of_day': float(current_time.hour),
                'requests_per_minute': random.uniform(80, 150),
                'ip': f"172.16.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'path': '/api/vulnerable',
                'user_agent': 'SecurityScanner/2.0'
            }
        
        elif anomaly_type == 'large_request':
            # Large request attack
            return {
                'timestamp': current_time.isoformat(),
                'method': 'POST',
                'status_code': random.choice([413, 500, 503]),  # Payload too large
                'status_code_numeric': float(random.choice([413, 500, 503])),
                'request_size': random.uniform(50000, 100000),  # Very large
                'response_time': random.uniform(3000, 10000),
                'hour_of_day': float(current_time.hour),
                'requests_per_minute': random.uniform(20, 60),
                'ip': f"203.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'path': '/api/upload',
                'user_agent': 'LargePayloadBot'
            }
        
        elif anomaly_type == 'slow_response':
            # Slow response anomaly
            return {
                'timestamp': current_time.isoformat(),
                'method': 'GET',
                'status_code': 200,
                'status_code_numeric': 200.0,
                'request_size': random.uniform(500, 2000),
                'response_time': random.uniform(10000, 20000),  # Very slow
                'hour_of_day': float(current_time.hour),
                'requests_per_minute': random.uniform(30, 80),
                'ip': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'path': '/api/heavy-computation',
                'user_agent': 'Mozilla/5.0 (Chrome)'
            }
        
        elif anomaly_type == 'night_activity':
            # Unusual night activity
            night_hour = random.choice([1, 2, 3, 4, 5])
            return {
                'timestamp': current_time.replace(hour=night_hour).isoformat(),
                'method': random.choice(['POST', 'PUT', 'DELETE']),
                'status_code': random.choice([200, 403, 404]),
                'status_code_numeric': float(random.choice([200, 403, 404])),
                'request_size': random.uniform(1000, 3000),
                'response_time': random.uniform(500, 2000),
                'hour_of_day': float(night_hour),
                'requests_per_minute': random.uniform(100, 200),  # High for night time
                'ip': f"198.51.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'path': '/admin/login',
                'user_agent': 'NightCrawler/1.0'
            }
        
        else:  # scan_attack
            # Systematic scanning
            return {
                'timestamp': current_time.isoformat(),
                'method': 'GET',
                'status_code': random.choice([404, 403, 200]),
                'status_code_numeric': float(random.choice([404, 403, 200])),
                'request_size': random.uniform(200, 800),
                'response_time': random.uniform(100, 500),
                'hour_of_day': float(current_time.hour),
                'requests_per_minute': random.uniform(150, 250),  # Systematic scanning
                'ip': f"185.220.{random.randint(1, 255)}.{random.randint(1, 255)}",  # Tor exit node range
                'path': random.choice([
                    '/admin', '/wp-admin', '/.env', '/config.php', 
                    '/backup.sql', '/test.php', '/shell.php'
                ]),
                'user_agent': 'Nmap/7.80'
            }
    
    def generate_log_entry(self):
        """Generate a single log entry (normal or anomaly)"""
        if random.random() < self.anomaly_probability:
            log_entry = self.generate_anomaly_log_entry()
            log_entry['is_anomaly'] = True
        else:
            log_entry = self.generate_normal_log_entry()
            log_entry['is_anomaly'] = False
        
        return log_entry
    
    def send_to_kafka(self, log_entry):
        """Send log entry to Kafka topic"""
        try:
            # Add some jitter to make it more realistic
            time.sleep(random.uniform(0.1, 2.0))
            
            future = self.producer.send(self.topic, log_entry)
            future.get(timeout=10)  # Wait for send to complete
            
            # Log the entry
            anomaly_indicator = "🚨" if log_entry.get('is_anomaly', False) else "✅"
            logger.info(f"{anomaly_indicator} Sent: {log_entry['method']} {log_entry['status_code']} "
                       f"({log_entry['response_time']:.0f}ms, {log_entry['request_size']:.0f}B)")
            
        except Exception as e:
            logger.error(f"❌ Failed to send message to Kafka: {e}")
    
    def run(self):
        """Start the server logs simulation"""
        logger.info("🖥️ Starting Server Logs Stream Simulator...")
        logger.info(f"   Topic: {self.topic}")
        logger.info(f"   Kafka: {self.kafka_bootstrap}")
        logger.info(f"   Anomaly Rate: {self.anomaly_probability:.1%}")
        
        self.running = True
        
        try:
            while self.running:
                # Generate and send log entry
                log_entry = self.generate_log_entry()
                self.send_to_kafka(log_entry)
                
        except KeyboardInterrupt:
            logger.info("🛑 Stopping simulator...")
        except Exception as e:
            logger.error(f"❌ Simulator error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the simulator"""
        self.running = False
        if self.producer:
            self.producer.close()
        logger.info("✅ Server Logs Simulator stopped")

def main():
    """Main function"""
    # Get configuration from environment variables
    kafka_bootstrap = os.getenv('KAFKA_BOOTSTRAP', 'kafka:9092')
    topic = 'server-logs'
    
    # Create and run simulator
    simulator = ServerLogsSimulator(kafka_bootstrap=kafka_bootstrap, topic=topic)
    simulator.run()

if __name__ == '__main__':
    main() 