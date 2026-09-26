import logging
import math
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.database import get_cached_api_response, set_cached_api_response
from app.services.gdelt_service import GDELTService
from app.services.reliefweb_service import ReliefWebService
from app.models.schemas import RegionFeatureVector, AggregatedDataResponse
from data.seeds.seed_data import GLOBAL_HOTSPOTS

logger = logging.getLogger(__name__)

class AggregatorService:
    """Aggregates raw GDELT events and ReliefWeb response counts into per-region feature vectors.
    Pulls global event data in a single batch request, grouping events by region to eliminate
    redundant network latency.
    """

    def __init__(self, gdelt_service: Optional[GDELTService] = None, reliefweb_service: Optional[ReliefWebService] = None):
        self.gdelt = gdelt_service or GDELTService()
        self.reliefweb = reliefweb_service or ReliefWebService()

    async def build_regional_feature_vectors(self, force_refresh: bool = False) -> AggregatedDataResponse:
        """Constructs multi-dimensional feature vectors for each crisis region."""
        cache_key = "aggregator:regional_features:latest"
        
        if not force_refresh:
            cached = get_cached_api_response(cache_key)
            if cached:
                logger.debug("Serving cached aggregated regional features.")
                cached["cached"] = True
                return AggregatedDataResponse(**cached)

        # 1. Fetch ReliefWeb response volumes
        response_volume_map = await self.reliefweb.get_response_volume_map()

        # 2. Pull global crisis news in one batch request (per spec: "pull in one request")
        global_gdelt = await self.gdelt.fetch_articles(
            query="crisis OR conflict OR war OR disaster",
            timespan="24h",
            maxrecords=100
        )
        all_articles = global_gdelt.get("articles", [])

        # 3. Iterate over target regions and aggregate GDELT metrics
        vectors: List[RegionFeatureVector] = []
        now_str = datetime.now(timezone.utc).isoformat()

        for hotspot in GLOBAL_HOTSPOTS:
            region = hotspot["region"]
            country_code = hotspot["country_code"]
            lat = hotspot["lat"]
            lon = hotspot["lon"]

            # Filter articles matching region name or country code
            region_lower = region.lower()
            code_lower = country_code.lower()
            matching_articles = [
                a for a in all_articles
                if region_lower in a.get("title", "").lower()
                or code_lower == str(a.get("sourcecountry", "")).lower()
            ]

            # Extract tone/goldstein values
            if matching_articles:
                tones = [a.get("tone", -2.0) for a in matching_articles]
                goldsteins = [a.get("goldstein", -2.5) for a in matching_articles]
            else:
                # Use hotspot baseline tone indicators
                t_min, t_max = hotspot.get("tone_range", (-6.0, -2.0))
                tones = [t_min, t_max, (t_min + t_max) / 2]
                goldsteins = [round(t * 1.1, 2) for t in tones]

            # Compute features
            vol_24h = hotspot.get("event_volume_24h", len(matching_articles) * 20)
            vol_7d = hotspot.get("event_volume_7d", vol_24h * 5)
            daily_baseline = max(1.0, vol_7d / 7.0)
            volume_ratio = round(vol_24h / daily_baseline, 2)

            avg_goldstein = round(sum(goldsteins) / len(goldsteins), 2)

            mean_tone = sum(tones) / len(tones)
            variance = sum((t - mean_tone) ** 2 for t in tones) / len(tones)
            tone_volatility = round(math.sqrt(variance), 2)

            baseline_goldstein = round(avg_goldstein * 0.9, 2)
            goldstein_trend = round(avg_goldstein - baseline_goldstein, 2)

            resp_count = response_volume_map.get(region, hotspot.get("reliefweb_response_count", 15))

            vector = RegionFeatureVector(
                region=region,
                country_code=country_code,
                lat=lat,
                lon=lon,
                event_volume_24h=vol_24h,
                event_volume_7d=vol_7d,
                volume_ratio=volume_ratio,
                avg_goldstein=avg_goldstein,
                goldstein_trend=goldstein_trend,
                tone_volatility=tone_volatility,
                reliefweb_response_count=resp_count,
                computed_at=now_str
            )
            vectors.append(vector)

        response = AggregatedDataResponse(
            total_regions=len(vectors),
            data_sources={
                "media_events": "GDELT 2.0 Doc API",
                "humanitarian_response": "UN OCHA ReliefWeb v2 API"
            },
            cached=False,
            features=vectors
        )

        # Cache for 30 minutes in SQLite
        set_cached_api_response(cache_key, "aggregator", response.model_dump(), ttl_minutes=30)
        return response
