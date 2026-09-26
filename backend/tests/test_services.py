import pytest
from app.services.gdelt_service import GDELTService
from app.services.reliefweb_service import ReliefWebService

@pytest.mark.asyncio
async def test_gdelt_service_structure():
    """Verify GDELT service returns standardized articles with tone and goldstein scores."""
    service = GDELTService()
    result = await service.fetch_articles(query="crisis", maxrecords=5, country="Sudan")
    
    assert "articles" in result
    assert "source" in result
    assert len(result["articles"]) > 0
    
    first = result["articles"][0]
    assert "title" in first
    assert "url" in first
    assert "tone" in first
    assert "goldstein" in first
    assert isinstance(first["tone"], (int, float))
    assert isinstance(first["goldstein"], (int, float))

@pytest.mark.asyncio
async def test_reliefweb_service_structure():
    """Verify ReliefWeb service returns standardized situation reports and response counts."""
    service = ReliefWebService()
    result = await service.fetch_reports(country="Sudan", limit=5)
    
    assert "reports" in result
    assert len(result["reports"]) > 0
    
    report = result["reports"][0]
    assert "id" in report
    assert "title" in report
    assert "primary_country" in report
    assert "source" in report
    
    vol_map = await service.get_response_volume_map()
    assert isinstance(vol_map, dict)
    assert "Sudan" in vol_map
    assert vol_map["Sudan"] > 0
