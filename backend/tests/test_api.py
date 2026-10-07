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

@pytest.mark.asyncio
async def test_auth_and_watchlist_lifecycle():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        test_email = f"analyst_{httpx.__version__}@crisispulse.org"
        # 1. Register
        reg_res = await client.post("/api/auth/register", json={
            "email": test_email,
            "password": "Password123!"
        })
        # If user already exists from previous test run, login instead
        if reg_res.status_code == 409:
            login_res = await client.post("/api/auth/login", json={
                "email": test_email,
                "password": "Password123!"
            })
            assert login_res.status_code == 200
            token = login_res.json()["token"]
        else:
            assert reg_res.status_code == 200
            token = reg_res.json()["token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Check /me
        me_res = await client.get("/api/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == test_email.lower()

        # 3. Add to watchlist
        add_res = await client.post("/api/watchlists", json={"country_or_crisis": "Sudan"}, headers=headers)
        assert add_res.status_code == 200
        assert "Sudan" in add_res.json()["items"]

        # 4. Get watchlist
        get_res = await client.get("/api/watchlists", headers=headers)
        assert get_res.status_code == 200
        assert "Sudan" in get_res.json()["items"]

        # 5. Remove from watchlist
        del_res = await client.delete("/api/watchlists/Sudan", headers=headers)
        assert del_res.status_code == 200
        assert "Sudan" not in del_res.json()["items"]

@pytest.mark.asyncio
async def test_trends_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/analytics/trends/Sudan")
        assert response.status_code == 200
        data = response.json()
        assert data["region"] == "Sudan"
        assert "current_gap_score" in data
        assert "trajectory" in data
        assert len(data["history"]) > 0

@pytest.mark.asyncio
async def test_export_csv_and_json():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        csv_res = await client.get("/api/analytics/export/csv")
        assert csv_res.status_code == 200
        assert "text/csv" in csv_res.headers["content-type"]
        assert "Region" in csv_res.text

        json_res = await client.get("/api/analytics/export/json")
        assert json_res.status_code == 200
        data = json_res.json()
        assert "results" in data
        assert len(data["results"]) > 0


