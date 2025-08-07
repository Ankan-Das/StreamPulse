# Pydantic Validation in Anomaly Detection Service

The anomaly detection service now includes comprehensive **Pydantic validation** for improved data quality, type safety, and automatic API documentation.

## 🚀 Features

### ✅ **Dynamic Input Validation**
- **Automatic Schema Generation**: Input schemas are dynamically created based on use case configuration
- **Smart Field Types**: Intelligent field type detection based on feature names
- **Validation Rules**: Built-in validation for common data patterns

### ✅ **Type Safety**
- **Strong Typing**: All endpoints use typed Pydantic models
- **Automatic Conversion**: Safe conversion between data types
- **Error Prevention**: Catch type errors before processing

### ✅ **Enhanced API Documentation**
- **Interactive Docs**: Automatic OpenAPI/Swagger documentation at `/docs`
- **Schema Endpoint**: GET `/schema` for programmatic schema access
- **Examples**: Built-in examples for each use case

## 🔧 Validation Rules

### **Feature-Based Validation**
The system automatically applies appropriate validation rules based on feature names:

| Feature Pattern | Validation Rule | Example |
|----------------|-----------------|---------|
| `*duration*` | `> 0` (positive) | `trip_duration: 1800.0` |
| `*distance*` | `≥ 0` (non-negative) | `trip_distance: 5.2` |
| `*amount*`, `*fare*`, `*price*` | `≥ 0` (non-negative) | `fare_amount: 15.50` |
| `*count*`, `*number*` | `≥ 0` (non-negative integer) | `passenger_count: 2` |
| `*time*` | `≥ 0` (non-negative) | `pickup_time: 1640995200` |
| `*rate*`, `*ratio*` | `≥ 0` (non-negative) | `tip_rate: 0.15` |

### **Custom Descriptions**
Each field gets a human-readable description automatically generated from the field name.

## 📡 API Endpoints

### **1. Service Information**
```http
GET /
```
**Response:**
```json
{
  "service": "Anomaly Detection API",
  "use_case": "nyc_taxi",
  "description": "NYC Taxi Trip Anomaly Detection",
  "features": ["trip_duration", "trip_distance", "fare_amount", "total_amount"]
}
```

### **2. Health Check**
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "use_case": "nyc_taxi"
}
```

### **3. Input Schema**
```http
GET /schema
```
**Response:**
```json
{
  "use_case": "nyc_taxi",
  "description": "NYC Taxi Trip Anomaly Detection",
  "input_schema": {
    "type": "object",
    "properties": {
      "trip_duration": {
        "type": "number",
        "exclusiveMinimum": 0,
        "description": "Trip Duration in seconds"
      },
      "trip_distance": {
        "type": "number",
        "minimum": 0,
        "description": "Trip Distance in miles/km"
      }
    },
    "required": ["trip_duration", "trip_distance", "fare_amount", "total_amount"]
  },
  "example_payload": {
    "trip_duration": 1800.0,
    "trip_distance": 5.2,
    "fare_amount": 15.50,
    "total_amount": 18.50
  }
}
```

### **4. Make Prediction**
```http
POST /predict
```
**Request Body:**
```json
{
  "trip_duration": 1800.0,
  "trip_distance": 5.2,
  "fare_amount": 15.50,
  "total_amount": 18.50
}
```
**Response:**
```json
{
  "anomaly": false,
  "use_case": "nyc_taxi",
  "features": {
    "trip_duration": 1800.0,
    "trip_distance": 5.2,
    "fare_amount": 15.50,
    "total_amount": 18.50
  },
  "confidence": 0.85
}
```

## ❌ Validation Errors

### **Missing Required Field**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "trip_duration"],
      "msg": "Field required",
      "input": {...}
    }
  ]
}
```

### **Invalid Value**
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "trip_duration"],
      "msg": "Input should be greater than 0",
      "input": -100.0
    }
  ]
}
```

### **Wrong Type**
```json
{
  "detail": [
    {
      "type": "float_parsing",
      "loc": ["body", "trip_distance"],
      "msg": "Input should be a valid number",
      "input": "not_a_number"
    }
  ]
}
```

## 🧪 Testing Validation

### **Run Test Script**
```bash
# Make sure the service is running
USE_CASE=nyc_taxi docker compose up

# Run validation tests
python test_pydantic_validation.py
```

### **Manual Testing Examples**

**✅ Valid Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_duration": 1800.0,
    "trip_distance": 5.2,
    "fare_amount": 15.50,
    "total_amount": 18.50
  }'
```

**❌ Invalid Request (Negative Duration):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_duration": -100.0,
    "trip_distance": 5.2,
    "fare_amount": 15.50,
    "total_amount": 18.50
  }'
```

**❌ Invalid Request (Missing Field):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_distance": 5.2,
    "fare_amount": 15.50,
    "total_amount": 18.50
  }'
```

## 🌐 Interactive Documentation

Visit **http://localhost:8000/docs** for:
- 📖 **Interactive API documentation**
- 🧪 **Try-it-out functionality**
- 📋 **Schema exploration**
- 💡 **Example requests and responses**

## 🎯 Benefits

1. **🛡️ Data Quality**: Prevents invalid data from reaching the model
2. **🐛 Error Prevention**: Catch issues early with clear error messages
3. **📚 Self-Documenting**: Automatic schema documentation
4. **🔒 Type Safety**: Strong typing throughout the application
5. **⚡ Performance**: Fast validation with clear error reporting
6. **🔄 Dynamic**: Automatically adapts to different use cases
7. **👩‍💻 Developer Experience**: Better tooling and IDE support

## 🔮 Future Enhancements

- **Custom Validators**: Use case-specific validation logic
- **Data Transformation**: Automatic unit conversion
- **Advanced Rules**: Cross-field validation (e.g., total ≥ fare)
- **Versioning**: Schema versioning for API evolution
- **Metrics**: Validation failure tracking in Prometheus

The Pydantic validation system makes the anomaly detection service more robust, user-friendly, and maintainable while providing excellent developer experience! 🚀 