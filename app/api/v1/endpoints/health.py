from fastapi import APIRouter
from app.db.session import engine
from app.core.logging import logger

router = APIRouter()

@router.get("/")
def health_check():
    health = {"status": "healthy"}
    
    # Check DB connection
    try:
        with engine.connect() as conn:
            pass
        health["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health["database"] = "disconnected"
        health["status"] = "unhealthy"

    return health
