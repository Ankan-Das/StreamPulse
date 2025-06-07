import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

X_train = np.column_stack([
    np.random.normal(200, 50, 1000),     # latency_ms
    np.random.uniform(0, 0.2, 1000)      # error_rate
])
model = IsolationForest(contamination=0.1)
model.fit(X_train)
joblib.dump(model, "model.joblib")