from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.db.models import PredictionHistory
import io
import csv

router = APIRouter()

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Get high-level analytics for the dashboard.
    """
    total_predictions = db.query(func.count(PredictionHistory.id)).scalar()
    total_frauds = db.query(func.count(PredictionHistory.id)).filter(PredictionHistory.prediction == 1).scalar()
    
    fraud_rate = 0.0
    if total_predictions > 0:
        fraud_rate = round((total_frauds / total_predictions) * 100, 2)
        
    # Get 10 most recent transactions
    recent = db.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).limit(10).all()
    
    recent_data = [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat(),
            "amount": r.amount,
            "prediction": r.prediction,
            "probability": round(r.probability, 4)
        } for r in recent
    ]
    
    return {
        "total_predictions": total_predictions,
        "total_frauds": total_frauds,
        "fraud_rate": fraud_rate,
        "recent_activity": recent_data
    }

@router.get("/export")
def export_history_csv(db: Session = Depends(get_db)):
    """
    Export the prediction history as a CSV file.
    """
    records = db.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["ID", "Timestamp", "Amount", "Prediction", "Probability", "Client IP"])
    
    # Write data
    for r in records:
        writer.writerow([r.id, r.timestamp, r.amount, r.prediction, r.probability, r.client_ip])
        
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=prediction_history.csv"}
    )
