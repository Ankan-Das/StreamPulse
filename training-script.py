import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

X_train = np.random.normal(200, 50, (1000, 2))  # Dummy latency/error
model = IsolationForest(contamination=0.05)
model.fit(X_train)
joblib.dump(model, "model.joblib")