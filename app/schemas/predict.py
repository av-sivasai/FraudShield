from pydantic import BaseModel, Field
from typing import List, Optional

class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float = Field(..., ge=0, description="Transaction amount must be positive")

class PredictionResponse(BaseModel):
    fraud_prediction: int = Field(..., description="1 if fraud, 0 otherwise")
    probability: float = Field(..., description="Probability of fraud")
    confidence_score: str = Field(..., description="High, Medium, or Low")

class BatchPredictionResponse(BaseModel):
    total_processed: int
    frauds_detected: int
    predictions: List[PredictionResponse]
