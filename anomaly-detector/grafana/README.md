# 📊 Grafana Dashboards

This directory contains Grafana dashboard configurations for the anomaly detection system.

## 🚀 Quick Setup

### 1. Import the Dashboard

1. **Open Grafana**: Navigate to `http://localhost:3000`
2. **Login**: Use default credentials (admin/admin)
3. **Import Dashboard**:
   - Click the "+" icon in the sidebar
   - Select "Import"
   - Click "Upload JSON file"
   - Upload `nyc-taxi-dashboard.json`
   - Select "Prometheus" as data source
   - Click "Import"

### 2. Configure Prometheus Data Source (if needed)

1. **Add Data Source**:
   - Go to Configuration → Data Sources
   - Click "Add data source"
   - Select "Prometheus"
   - URL: `http://prometheus:9090`
   - Click "Save & Test"

## 📁 Available Dashboards

### 🚕 NYC Taxi Anomaly Detection (`nyc-taxi-dashboard.json`)

**Features:**
- 🚨 Real-time anomaly status indicator
- 📊 Trip processing statistics  
- 💰 Financial metrics (fare, total amount)
- 🚗 Trip characteristics (duration, distance)
- 📈 Historical trends and patterns
- ⚡ Processing performance metrics

**Key Panels:**
- **Current Anomaly Status** - Large color-coded indicator
- **Trip Statistics** - Total processed, anomalies found, anomaly rate
- **Financial Info** - Current fare and total amounts
- **Trip Info** - Duration and distance metrics
- **Timeline Charts** - Historical anomaly detection
- **Trend Analysis** - All feature trends over time
- **Performance Metrics** - Processing and anomaly detection rates

**Thresholds:**
- 🟢 **Normal**: < 5% anomaly rate
- 🟡 **Warning**: 5-15% anomaly rate  
- 🔴 **Critical**: > 15% anomaly rate

## 🎯 Usage Tips

### **Real-time Monitoring**
- Dashboard refreshes every 10 seconds
- Set time range to "Last 30 minutes" for active monitoring
- Watch the anomaly timeline for patterns

### **Troubleshooting**
- If panels show "No data", check Prometheus targets at `http://localhost:9090/targets`
- Verify services are running: `docker compose ps`
- Check metric endpoints:
  - FastAPI ML Service: `http://localhost:8001/metrics`
  - Processor: `http://localhost:9000/metrics`

### **Customization**
- Edit panels to adjust thresholds
- Add new panels for additional metrics
- Modify time ranges and refresh intervals
- Create alerts for critical anomaly rates

## 📱 Mobile Support

The dashboard is responsive and works on mobile devices:
- **Portrait mode**: Panels stack vertically
- **Landscape mode**: Side-by-side layout
- **Touch-friendly**: Large buttons and clear text

## 🔔 Setting Up Alerts (Optional)

### Example Alert Rules:

1. **High Anomaly Rate**:
   ```
   Query: (nyc_taxi_anomalies_total / nyc_taxi_total_messages_total) * 100 > 10
   Condition: Anomaly rate above 10%
   ```

2. **Service Down**:
   ```
   Query: up{job="fastapi-ml-service"} == 0
   Condition: ML service unavailable
   ```

## 🚀 Performance Tips

1. **Time Ranges**: Use appropriate ranges (30m for real-time, 6h for trends)
2. **Refresh Rates**: 10s for monitoring, 1m for analysis
3. **Panel Limits**: Keep under 20 panels per dashboard
4. **Query Optimization**: Use rate() for counter metrics

## 🎨 Color Scheme

- 🟢 **Green**: Normal operations, good performance
- 🟡 **Yellow**: Warning thresholds, attention needed
- 🟠 **Orange**: High values, monitor closely  
- 🔴 **Red**: Critical values, immediate action needed
- 🔵 **Blue**: Neutral information, counts and totals

## 📚 Metrics Reference

### **Core Metrics:**
- `nyc_taxi_latest_is_anomaly` - Current anomaly status (0=normal, 1=anomaly)
- `nyc_taxi_total_messages_total` - Total trips processed
- `nyc_taxi_anomalies_total` - Total anomalies detected

### **Feature Metrics:**
- `nyc_taxi_latest_trip_duration` - Latest trip duration (seconds)
- `nyc_taxi_latest_trip_distance` - Latest trip distance (miles)
- `nyc_taxi_latest_fare_amount` - Latest fare amount ($)
- `nyc_taxi_latest_total_amount` - Latest total amount ($)

### **Derived Metrics:**
- Processing rate: `rate(nyc_taxi_total_messages_total[1m])`
- Anomaly rate: `rate(nyc_taxi_anomalies_total[5m])`
- Anomaly percentage: `(anomalies_total / total_messages) * 100`

---

🎉 **Happy Monitoring!** Your NYC taxi anomaly detection system is now fully observable with this comprehensive dashboard! 