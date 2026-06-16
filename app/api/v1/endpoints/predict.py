from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.predict import Transaction, PredictionResponse, BatchPredictionResponse
from app.services.prediction import process_prediction
from app.db.session import get_db
import pandas as pd
import io

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
def predict_fraud(
    request: Request,
    transaction: Transaction,
    db: Session = Depends(get_db)
):
    """
    Predict if a single transaction is fraudulent.
    """
    client_ip = request.client.host if request.client else None
    try:
        return process_prediction(transaction, db, client_ip)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Predict fraud for a batch of transactions via CSV upload.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # We need the 30 features
        expected_columns = [f"V{i}" for i in range(1, 29)] + ["Time", "Amount"]
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_cols}")

        client_ip = request.client.host if request.client else None
        
        predictions = []
        frauds_detected = 0
        
        for _, row in df.iterrows():
            transaction_dict = row.to_dict()
            transaction = Transaction(**transaction_dict)
            res = process_prediction(transaction, db, client_ip)
            predictions.append(res)
            if res.fraud_prediction == 1:
                frauds_detected += 1
                
        return BatchPredictionResponse(
            total_processed=len(predictions),
            frauds_detected=frauds_detected,
            predictions=predictions
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")
