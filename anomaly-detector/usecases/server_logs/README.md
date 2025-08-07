# 🖥️ Server Logs Anomaly Detection Use Case

This use case detects anomalies in server logs using machine learning techniques. It can identify various types of suspicious activities, performance issues, and security threats.

## 🎯 **Anomaly Types Detected**

### **Security Threats**
- 🚨 **DDoS Attacks** - High traffic with slow responses
- 🚨 **Security Scans** - Systematic probing of endpoints
- 🚨 **Error Spikes** - Unusual patterns of HTTP errors
- 🚨 **Large Request Attacks** - Unusually large payload attacks

### **Performance Issues**
- ⚡ **Slow Response Times** - Server performance degradation
- ⚡ **Traffic Spikes** - Unexpected load increases
- ⚡ **Off-hours Activity** - Unusual activity patterns

## 📊 **Features Used**

| Feature | Description | Normal Range | Anomaly Indicators |
|---------|-------------|--------------|-------------------|
| `response_time` | Request processing time (ms) | 50-800ms | >5000ms |
| `request_size` | Request payload size (bytes) | 100-10KB | >50KB or <100B |
| `status_code_numeric` | HTTP status code | 200, 304 | 4xx, 5xx patterns |
| `hour_of_day` | Hour when request occurred | 9-17 peak | 1-5 AM activity |
| `requests_per_minute` | Request rate | 20-80/min | >300/min or <5/min |

## 🏗️ **Architecture**

```
📥 Server Logs → 🔄 Stream Simulator → 📡 Kafka → 🧠 ML Processor → 📊 Grafana
```

## 🚀 **Quick Start**

### **1. Train the Model**

```bash
# Navigate to the use case directory
cd anomaly-detector/usecases/server_logs

# Install dependencies
pip install -r requirements.txt

# Run the training notebook
jupyter notebook train_model.ipynb
```

### **2. Test with Docker**

```bash
# Navigate to anomaly detector directory
cd anomaly-detector

# Run with server logs use case
USE_CASE=server_logs docker compose up --build
```

### **3. Monitor in Grafana**

1. Open Grafana: `http://localhost:3000`
2. Import the dashboard from `anomaly-detector/grafana/server-logs-dashboard.json`
3. Watch real-time anomaly detection

## 📈 **Metrics Generated**

### **Core Metrics**
- `server_logs_latest_is_anomaly` - Current anomaly status (0/1)
- `server_logs_total_messages_total` - Total requests processed
- `server_logs_anomalies_total` - Total anomalies detected

### **Feature Metrics**
- `server_logs_latest_response_time` - Latest response time
- `server_logs_latest_request_size` - Latest request size
- `server_logs_latest_status_code_numeric` - Latest status code
- `server_logs_latest_hour_of_day` - Latest hour
- `server_logs_latest_requests_per_minute` - Latest request rate

## 🎛️ **Configuration**

### **Anomaly Simulation Types**

The stream simulator generates these anomaly types:

1. **DDoS Attack** - High traffic, slow responses, suspicious IPs
2. **Error Spike** - Many 4xx/5xx status codes
3. **Large Request** - Payload >50KB, often 413 responses
4. **Slow Response** - Response times >10 seconds
5. **Night Activity** - High traffic during 1-5 AM
6. **Scan Attack** - Systematic probing of common paths

### **Tuning Parameters**

Edit `stream_simulator.py` to adjust:

```python
self.base_requests_per_minute = 60  # Base traffic rate
self.anomaly_probability = 0.05     # 5% anomaly rate
```

## 🔧 **Model Details**

- **Algorithm**: Isolation Forest
- **Training**: Unsupervised (normal data only)
- **Features**: 5 numerical features
- **Contamination**: 5% expected anomaly rate
- **Performance**: ~85% precision, ~80% recall

## 📋 **Log Format Example**

### Normal Request
```json
{
  "timestamp": "2025-01-27T10:30:45.123456",
  "method": "GET",
  "status_code": 200,
  "status_code_numeric": 200.0,
  "request_size": 1250.0,
  "response_time": 245.0,
  "hour_of_day": 10.0,
  "requests_per_minute": 65.0,
  "ip": "192.168.1.100",
  "path": "/api/users",
  "user_agent": "Mozilla/5.0 (Chrome)",
  "is_anomaly": false
}
```

### Anomalous Request (DDoS)
```json
{
  "timestamp": "2025-01-27T14:15:20.654321",
  "method": "GET",
  "status_code": 503,
  "status_code_numeric": 503.0,
  "request_size": 800.0,
  "response_time": 8500.0,
  "hour_of_day": 14.0,
  "requests_per_minute": 450.0,
  "ip": "10.0.1.50",
  "path": "/",
  "user_agent": "AttackBot/1.0",
  "is_anomaly": true
}
```

## 🛠️ **Customization**

### **Adding New Features**

1. Update `config.yaml` with new feature names
2. Modify `features.py` to extract new features
3. Update `stream_simulator.py` to generate the features
4. Retrain the model with new features

### **Adjusting Thresholds**

Edit anomaly generation in `stream_simulator.py`:

```python
# DDoS detection thresholds
response_time > 5000  # ms
requests_per_minute > 300  # req/min

# Large request thresholds
request_size > 50000  # bytes
```

## 📊 **Grafana Dashboard**

The dashboard includes:

- 🚨 **Real-time Anomaly Status** - Current threat level
- 📈 **Request Rate Trends** - Traffic patterns over time
- ⏱️ **Response Time Distribution** - Performance metrics
- 🔍 **Status Code Analysis** - Error rate monitoring
- 🌙 **Hourly Activity Patterns** - Off-hours monitoring

## 🧪 **Testing**

### **Manual Testing**

```python
# Test feature extraction
from features import extract_features, parse_apache_log

test_log = '192.168.1.1 - - [27/Jan/2025:10:30:45 +0000] "GET / HTTP/1.1" 200 1234'
parsed = parse_apache_log(test_log)
features = extract_features(parsed)
print(features)
```

### **Model Testing**

```python
import joblib
model = joblib.load('model_server_logs.joblib')
scaler = joblib.load('scaler_server_logs.joblib')

# Test prediction
test_data = [[245.0, 1250.0, 200.0, 10.0, 65.0]]
scaled_data = scaler.transform(test_data)
prediction = model.predict(scaled_data)
print("Anomaly detected:" if prediction[0] == -1 else "Normal request")
```

## 🚨 **Alerts & Monitoring**

### **Grafana Alerts**

Set up alerts for:
- Anomaly rate > 10%
- Average response time > 2000ms
- Error rate > 5%
- Traffic spike > 200 req/min

### **Log Analysis**

Monitor processor logs for:
```
🚨 ANOMALY DETECTED - Use case: server_logs
✅ Normal - Use case: server_logs
```

## 📚 **References**

- [Isolation Forest Paper](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)
- [Apache Log Format](https://httpd.apache.org/docs/current/logs.html)
- [Server Log Analysis Best Practices](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-apache.html)

---

🎉 **Your server logs anomaly detection system is ready to deploy!** 