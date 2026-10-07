import pytest
from app.services.analytics_engine import AnalyticsEngine
from app.models.schemas import RegionFeatureVector

@pytest.fixture
def sample_feature_vectors():
    return [
        RegionFeatureVector(
            region="Sudan",
            country_code="SD",
            lat=12.8628,
            lon=30.2176,
            event_volume_24h=480,
            event_volume_7d=2150,
            volume_ratio=1.56,
            avg_goldstein=-7.2,
            goldstein_trend=-0.72,
            tone_volatility=1.8,
            reliefweb_response_count=12,
            computed_at="2026-09-26T12:00:00Z"
        ),
        RegionFeatureVector(
            region="Ukraine",
            country_code="UA",
            lat=48.3794,
            lon=31.1656,
            event_volume_24h=1200,
            event_volume_7d=8400,
            volume_ratio=1.0,
            avg_goldstein=-4.5,
            goldstein_trend=0.1,
            tone_volatility=1.2,
            reliefweb_response_count=85,
            computed_at="2026-09-26T12:00:00Z"
        ),
        RegionFeatureVector(
            region="Haiti",
            country_code="HT",
            lat=18.9712,
            lon=-72.2852,
            event_volume_24h=310,
            event_volume_7d=1300,
            volume_ratio=1.67,
            avg_goldstein=-8.0,
            goldstein_trend=-1.2,
            tone_volatility=2.4,
            reliefweb_response_count=8,
            computed_at="2026-09-26T12:00:00Z"
        ),
        RegionFeatureVector(
            region="Somalia",
            country_code="SO",
            lat=5.1521,
            lon=46.1996,
            event_volume_24h=180,
            event_volume_7d=1200,
            volume_ratio=1.05,
            avg_goldstein=-4.1,
            goldstein_trend=0.0,
            tone_volatility=1.1,
            reliefweb_response_count=26,
            computed_at="2026-09-26T12:00:00Z"
        ),
        RegionFeatureVector(
            region="Gaza",
            country_code="PS",
            lat=31.3547,
            lon=34.3088,
            event_volume_24h=2100,
            event_volume_7d=11000,
            volume_ratio=1.34,
            avg_goldstein=-8.8,
            goldstein_trend=-0.5,
            tone_volatility=2.8,
            reliefweb_response_count=45,
            computed_at="2026-09-26T12:00:00Z"
        )
    ]

def test_gap_score_bounds_and_ranking(sample_feature_vectors):
    engine = AnalyticsEngine()
    
    # Calculate for each
    scores = {}
    for vec in sample_feature_vectors:
        score = engine.calculate_gap_score(vec)
        scores[vec.region] = score
        assert 0.0 <= score <= 10.0, f"Score {score} out of bounds for {vec.region}"
    
    # Haiti and Sudan have severe conflict and very low response counts (under-funded)
    # Their gap scores should reflect high disparity compared to well-responded areas
    assert scores["Haiti"] > 5.0
    assert scores["Sudan"] > 5.0

def test_classification_archetypes(sample_feature_vectors):
    engine = AnalyticsEngine()
    
    for vec in sample_feature_vectors:
        score = engine.calculate_gap_score(vec)
        cat = engine.classify_hotspot(vec, score)
        assert cat in [
            "Neglected Emergency",
            "Escalating Hotspot",
            "Protracted Crisis",
            "Stabilized Response"
        ]

def test_anomaly_detection(sample_feature_vectors):
    engine = AnalyticsEngine()
    anomalies = engine.detect_anomalies(sample_feature_vectors)
    
    assert isinstance(anomalies, dict)
    assert len(anomalies) == len(sample_feature_vectors)
    for k, v in anomalies.items():
        assert isinstance(v, bool)

def test_process_and_persist(sample_feature_vectors):
    engine = AnalyticsEngine()
    results = engine.process_and_persist(sample_feature_vectors)
    
    assert len(results) == len(sample_feature_vectors)
    first = results[0]
    assert "region" in first
    assert "gap_score" in first
    assert "category" in first
    assert "is_anomaly" in first

    # Verify retrieval
    persisted = engine.get_persisted_classifications()
    assert len(persisted) > 0

def test_explain_classification(sample_feature_vectors):
    engine = AnalyticsEngine()
    results = engine.process_and_persist(sample_feature_vectors)
    assert len(results) > 0
    first = results[0]
    assert "explainability" in first
    expl = first["explainability"]
    assert "archetype" in expl
    assert "primary_reason" in expl
    assert "criteria" in expl
    assert "feature_drivers" in expl
    assert len(expl["criteria"]) > 0
    assert len(expl["feature_drivers"]) == 5
