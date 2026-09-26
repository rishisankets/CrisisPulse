import pytest
import sqlite3
from datetime import datetime, timezone
from app.database import (
    init_db,
    get_db_connection,
    set_cached_api_response,
    get_cached_api_response,
    record_gap_score,
    get_latest_gap_scores
)

def test_database_init():
    """Verify all tables from specification are created."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        
        expected = [
            "users",
            "watchlists",
            "gap_score_cache",
            "region_classifications",
            "session_tokens",
            "api_cache"
        ]
        for t in expected:
            assert t in tables, f"Expected table '{t}' was not created."

def test_api_cache_roundtrip():
    """Verify setting and getting cached API responses with TTL."""
    init_db()
    test_key = "test:query:123"
    test_data = {"status": "ok", "items": [1, 2, 3]}
    
    set_cached_api_response(test_key, "test_source", test_data, ttl_minutes=10)
    cached = get_cached_api_response(test_key)
    
    assert cached is not None
    assert cached["status"] == "ok"
    assert cached["items"] == [1, 2, 3]

def test_gap_score_record_and_retrieve():
    """Verify recording and querying latest gap scores."""
    init_db()
    record_gap_score("Sudan", 8.4, 480, 38)
    record_gap_score("Ukraine", 6.2, 1250, 142)
    
    latest = get_latest_gap_scores()
    assert len(latest) >= 2
    regions = [r["region"] for r in latest]
    assert "Sudan" in regions
    assert "Ukraine" in regions
