from typing import List, Optional
from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Query, HTTPException

from app.services.gdelt_service import GDELTService
from app.services.reliefweb_service import ReliefWebService
from app.services.aggregator import AggregatorService
from app.services.analytics_engine import AnalyticsEngine
from app.models.schemas import (
    AnalyticsOverviewResponse,
    RegionAnalyticsItem,
    GapScoreRankingItem
)
from app.database import get_latest_gap_scores

router = APIRouter(prefix="/analytics", tags=["Analytics & ML Layer"])

gdelt_service = GDELTService()
reliefweb_service = ReliefWebService()
aggregator_service = AggregatorService(gdelt_service, reliefweb_service)
analytics_engine = AnalyticsEngine()

@router.get("/overview", response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(
    force_refresh: bool = Query(False, description="Recompute and refresh feature vectors and analytics")
):
    """Computes comprehensive crisis analytics:
    - Calculates Gap Scores for each active crisis region
    - Runs Isolation Forest anomaly detection
    - Assigns crisis archetypes (Neglected Emergency, Escalating Hotspot, etc.)
    - Persists snapshots to SQLite database
    """
    aggregated = await aggregator_service.build_regional_feature_vectors(force_refresh=force_refresh)
    results = analytics_engine.process_and_persist(aggregated.features)
    
    neglected_count = sum(1 for r in results if r["category"] == "Neglected Emergency")
    escalating_count = sum(1 for r in results if r["category"] == "Escalating Hotspot")
    anomalies_detected = sum(1 for r in results if r["is_anomaly"])

    return AnalyticsOverviewResponse(
        timestamp=datetime.now(timezone.utc).isoformat(),
        total_analyzed=len(results),
        neglected_count=neglected_count,
        escalating_count=escalating_count,
        anomalies_detected=anomalies_detected,
        results=[RegionAnalyticsItem(**r) for r in results]
    )

@router.get("/gap-scores", response_model=List[GapScoreRankingItem])
async def get_gap_score_rankings():
    """Retrieves the latest attention-response gap score ranking across all monitored regions."""
    records = get_latest_gap_scores()
    return [GapScoreRankingItem(**r) for r in records]

@router.get("/anomalies", response_model=List[RegionAnalyticsItem])
async def get_anomalies(
    force_refresh: bool = Query(False, description="Recompute and refresh features before checking anomalies")
):
    """Returns only regions identified as statistical or behavioural anomalies by Isolation Forest."""
    aggregated = await aggregator_service.build_regional_feature_vectors(force_refresh=force_refresh)
    results = analytics_engine.process_and_persist(aggregated.features)
    anomalous = [r for r in results if r["is_anomaly"]]
    return [RegionAnalyticsItem(**r) for r in anomalous]

@router.get("/classifications")
async def get_classifications():
    """Returns the most recent persisted category assignments and anomaly flags."""
    return analytics_engine.get_persisted_classifications()

@router.get("/explain/{region}")
async def explain_region_classification(region: str):
    """Returns full ML interpretability breakdown, decision path, and feature attributions for a given crisis region."""
    aggregated = await aggregator_service.build_regional_feature_vectors(force_refresh=False)
    results = analytics_engine.process_and_persist(aggregated.features)
    matched = next((r for r in results if r["region"].lower() == region.lower() or r["country_code"].lower() == region.lower()), None)
    if not matched:
        raise HTTPException(status_code=404, detail=f"Crisis region '{region}' not found")
    return {
        "region": matched["region"],
        "country_code": matched["country_code"],
        "gap_score": matched["gap_score"],
        "category": matched["category"],
        "is_anomaly": matched["is_anomaly"],
        "explainability": matched["explainability"]
    }
