#!/bin/bash

echo "🚀 Testing Multi-Use Case Anomaly Detection System"
echo "=================================================="

# Test 1: Check if required files exist
echo "📁 Checking file structure..."

required_files=(
    "usecases/nyc_taxi/config.yaml"
    "usecases/nyc_taxi/features.py"
    "usecases/nyc_taxi/model_taxi.joblib"
    "usecases/nyc_taxi/scaler_taxi.joblib"
    "fastapi-ml-service/main.py"
    "processor/main.py"
    "docker-compose.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Test 2: Validate YAML configuration
echo ""
echo "🔧 Validating configuration..."
python3 -c "
import yaml
try:
    with open('usecases/nyc_taxi/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print('✅ NYC taxi config.yaml is valid')
    print(f'   - Name: {config[\"name\"]}')
    print(f'   - Features: {config[\"features\"]}')
    print(f'   - Kafka topic: {config[\"kafka\"][\"topic\"]}')
except Exception as e:
    print(f'❌ Error in config.yaml: {e}')
    exit(1)
"

# Test 3: Check if features module is importable
echo ""
echo "🐍 Testing features module..."
python3 -c "
import sys
sys.path.append('usecases/nyc_taxi')
try:
    import features
    test_payload = {
        'trip_duration': 1000,
        'trip_distance': 5.0,
        'fare_amount': 15.50,
        'total_amount': 18.50
    }
    
    # Test validation
    if features.validate_payload(test_payload):
        print('✅ Payload validation works')
    else:
        print('❌ Payload validation failed')
        exit(1)
    
    # Test feature extraction
    extracted = features.extract_features(test_payload)
    print(f'✅ Feature extraction works: {extracted.shape}')
    
except Exception as e:
    print(f'❌ Error importing features module: {e}')
    exit(1)
"

echo ""
echo "🎉 All tests passed! Your multi-use case system is ready."
echo ""
echo "🚦 To start the system:"
echo "   USE_CASE=nyc_taxi docker-compose up"
echo ""
echo "🌐 Access points:"
echo "   - FastAPI: http://localhost:8000"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3000"
echo ""
echo "📚 Check README_Multi_UseCase.md for adding new use cases!" 