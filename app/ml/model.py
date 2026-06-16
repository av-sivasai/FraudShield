import joblib
import pandas as pd
from app.core.config import settings
from app.core.logging import logger
import os

class MLModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_models()

    def load_models(self):
        try:
            if os.path.exists(settings.MODEL_PATH) and os.path.exists(settings.SCALER_PATH):
                self.model = joblib.load(settings.MODEL_PATH)
                self.scaler = joblib.load(settings.SCALER_PATH)
                logger.info("ML Models loaded successfully.")
            else:
                logger.warning("ML Models not found. Using mock models for demonstration.")
                self.model = MockModel()
                self.scaler = MockScaler()
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.model = MockModel()
            self.scaler = MockScaler()

    def predict(self, df: pd.DataFrame):
        scaled_data = self.scaler.transform(df)
        prediction = self.model.predict(scaled_data)
        probability = self.model.predict_proba(scaled_data)
        return int(prediction[0]), float(probability[0][1])

class MockModel:
    def predict(self, X):
        return [0] * len(X)
    
    def predict_proba(self, X):
        return [[0.9, 0.1]] * len(X)

class MockScaler:
    def transform(self, X):
        return X

ml_model = MLModel()
