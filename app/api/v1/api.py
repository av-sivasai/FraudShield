from fastapi import APIRouter
from app.api.v1.endpoints import predict, health, model_info, analytics

api_router = APIRouter()
api_router.include_router(predict.router, prefix="/predict", tags=["prediction"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(model_info.router, prefix="/model-info", tags=["model"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
