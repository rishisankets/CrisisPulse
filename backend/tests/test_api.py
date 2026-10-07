import pytest
import httpx
from app.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["app"] == "CrisisPulse"
        assert "documentation" in data

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"

@pytest.mark.asyncio
async def test_gdelt_raw_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/gdelt/raw?query=crisis&maxrecords=5")
        assert response.status_code == 200
        data = response.json()
        assert "articles" in data
        assert len(data["articles"]) > 0

@pytest.mark.asyncio
async def test_reliefweb_raw_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/reliefweb/raw?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "reports" in data
        assert len(data["reports"]) > 0

@pytest.mark.asyncio
async def test_aggregated_data_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/data/aggregated")
        assert response.status_code == 200
        data = response.json()
        assert data["total_regions"] > 0
        assert len(data["features"]) > 0
        assert "event_volume_24h" in data["features"][0]
        assert "avg_goldstein" in data["features"][0]

@pytest.mark.asyncio
async def test_analytics_overview_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_analyzed" in data
        assert "results" in data
        assert len(data["results"]) > 0
        first = data["results"][0]
        assert "gap_score" in first
        assert "category" in first
        assert "is_anomaly" in first

@pytest.mark.asyncio
async def test_gap_scores_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/analytics/gap-scores")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "gap_score" in data[0]
            assert "region" in data[0]

@pytest.mark.asyncio
async def test_anomalies_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/analytics/anomalies")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_classifications_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/analytics/classifications")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_explain_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/analytics/explain/Sudan")
        assert response.status_code == 200
        data = response.json()
        assert data["region"] == "Sudan"
        assert "explainability" in data
        assert "primary_reason" in data["explainability"]
        assert "feature_drivers" in data["explainability"]


