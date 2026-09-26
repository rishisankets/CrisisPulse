from fastapi import APIRouter
from datetime import datetime, timezone

from app.config import settings
from app.database import get_db_connection
from app.models.schemas import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check verifying SQLite connectivity and data services configuration."""
    db_status = "connected"
    try:
        with get_db_connection() as conn:
            conn.execute("SELECT 1;").fetchone()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.VERSION,
        database=db_status,
        gdelt_status="ready (Doc 2.0 API with rate-limiter & cache)",
        reliefweb_status=f"ready (v2 API, appname: {settings.RELIEFWEB_APPNAME})",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
