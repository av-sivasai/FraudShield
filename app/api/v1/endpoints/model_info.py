from fastapi import APIRouter
from app.ml.model import ml_model

router = APIRouter()

@router.get("/")
def get_model_info():
    """
    Returns metadata about the deployed model.
    """
    model_type = type(ml_model.model).__name__ if ml_model.model else "Unknown"
    is_mock = model_type == "MockModel"
    
    return {
        "model_type": model_type,
        "is_mock": is_mock,
        "version": "1.0.0",
        "features_required": 30,
        "description": "Random Forest model for Credit Card Fraud Detection. Uses PCA features V1-V28, Time, and Amount."
    }
