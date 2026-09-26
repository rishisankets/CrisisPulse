from typing import Optional
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Query

from app.services.gdelt_service import GDELTService
from app.services.reliefweb_service import ReliefWebService
from app.services.aggregator import AggregatorService
from app.models.schemas import AggregatedDataResponse

router = APIRouter(tags=["Data Layer"])

gdelt_service = GDELTService()
reliefweb_service = ReliefWebService()
aggregator_service = AggregatorService(gdelt_service, reliefweb_service)

@router.get("/gdelt/raw")
async def get_raw_gdelt_events(
    query: str = Query("crisis", description="Keywords to query in GDELT articles"),
    timespan: str = Query("24h", description="Timespan window: 24h, 7d, etc."),
    country: Optional[str] = Query(None, description="Country name or ISO code filter"),
    maxrecords: int = Query(25, ge=1, le=250, description="Max articles to retrieve")
):
    """Fetches raw/normalized GDELT global conflict news events with automatic caching and 429 backoff."""
    return await gdelt_service.fetch_articles(
        query=query,
        timespan=timespan,
        maxrecords=maxrecords,
        country=country
    )

@router.get("/reliefweb/raw")
async def get_raw_reliefweb_reports(
    country: Optional[str] = Query(None, description="Country filter for humanitarian reports"),
    query: Optional[str] = Query(None, description="Search query terms"),
    limit: int = Query(20, ge=1, le=100, description="Number of reports to fetch")
):
    """Fetches raw/normalized UN OCHA ReliefWeb v2 situation reports and emergency appeals."""
    return await reliefweb_service.fetch_reports(
        country=country,
        query=query,
        limit=limit
    )

@router.get("/data/aggregated", response_model=AggregatedDataResponse)
async def get_aggregated_features(
    refresh: bool = Query(False, description="Bypass cache and recompute features")
):
    """Computes and returns per-region multi-dimensional feature vectors fusing GDELT and ReliefWeb data."""
    return await aggregator_service.build_regional_feature_vectors(force_refresh=refresh)
