from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Credit Card Fraud Detection API"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "random_forest_model.pkl"
    SCALER_PATH: str = "scaler.pkl"
    DATABASE_URL: str = "sqlite:///./data/predictions.db"
    RATE_LIMIT: str = "100/minute"
    
    class Config:
        env_file = ".env"

settings = Settings()
