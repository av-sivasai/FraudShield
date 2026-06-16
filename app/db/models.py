from sqlalchemy import Column, Integer, Float, DateTime, String
from app.db.session import Base
from datetime import datetime

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float)
    prediction = Column(Integer)
    probability = Column(Float)
    client_ip = Column(String, index=True, nullable=True)
