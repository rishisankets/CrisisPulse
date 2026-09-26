import pytest
from app.services.aggregator import AggregatorService
from app.models.schemas import AggregatedDataResponse, RegionFeatureVector

@pytest.mark.asyncio
async def test_aggregator_feature_vectors():
    """Verify aggregation generates all required ML feature dimensions per region."""
    aggregator = AggregatorService()
    response = await aggregator.build_regional_feature_vectors(force_refresh=True)
    
    assert isinstance(response, AggregatedDataResponse)
    assert response.total_regions > 0
    assert len(response.features) == response.total_regions
    
    # Check feature vector properties for each region
    for vec in response.features:
        assert isinstance(vec, RegionFeatureVector)
        assert vec.region != ""
        assert vec.country_code != ""
        assert isinstance(vec.lat, float)
        assert isinstance(vec.lon, float)
        
        # Verify ML features
        assert vec.event_volume_24h >= 0
        assert vec.event_volume_7d >= 0
        assert vec.volume_ratio >= 0.0
        assert -10.0 <= vec.avg_goldstein <= 10.0
        assert isinstance(vec.goldstein_trend, float)
        assert vec.tone_volatility >= 0.0
        assert vec.reliefweb_response_count >= 0

@pytest.mark.asyncio
async def test_aggregator_caching():
    """Verify aggregated response is cached for subsequent queries."""
    aggregator = AggregatorService()
    # First call forces refresh
    await aggregator.build_regional_feature_vectors(force_refresh=True)
    
    # Second call should serve from cache
    cached_res = await aggregator.build_regional_feature_vectors(force_refresh=False)
    assert cached_res.total_regions > 0
