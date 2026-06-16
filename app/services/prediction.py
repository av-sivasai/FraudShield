import pandas as pd
from app.schemas.predict import Transaction, PredictionResponse
from app.ml.model import ml_model
from app.db.models import PredictionHistory
from sqlalchemy.orm import Session
from app.core.logging import logger

def get_confidence_score(probability: float) -> str:
    if probability >= 0.8 or probability <= 0.2:
        return "High"
    elif probability >= 0.6 or probability <= 0.4:
        return "Medium"
    else:
        return "Low"

def process_prediction(transaction: Transaction, db: Session, client_ip: str = None) -> PredictionResponse:
    df = pd.DataFrame([transaction.model_dump()])
    
    prediction, probability = ml_model.predict(df)
    confidence = get_confidence_score(probability)
    
    # Save to history
    try:
        history_entry = PredictionHistory(
            amount=transaction.Amount,
            prediction=prediction,
            probability=probability,
            client_ip=client_ip
        )
        db.add(history_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to save prediction history: {e}")
        db.rollback()

    return PredictionResponse(
        fraud_prediction=prediction,
        probability=probability,
        confidence_score=confidence
    )
