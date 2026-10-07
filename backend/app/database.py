import sqlite3
import json
import logging
import uuid
from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Any, Generator, List, Dict

from app.config import settings

logger = logging.getLogger(__name__)

def get_db_path() -> Path:
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    return settings.DATABASE_PATH

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite connections with WAL mode and row factory."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path), timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db() -> None:
    """Initializes SQLite database tables and indexes per CrisisPulse specification."""
    logger.info(f"Initializing database at: {get_db_path()}")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 2. watchlists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watchlists (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                country_or_crisis TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_watchlists_user ON watchlists(user_id);
        """)
        
        # 3. gap_score_cache
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gap_score_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                gap_score REAL NOT NULL,
                media_volume INTEGER NOT NULL,
                response_volume INTEGER NOT NULL,
                computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gap_score_region ON gap_score_cache(region, computed_at DESC);
        """)
        
        # 4. region_classifications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS region_classifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                category TEXT NOT NULL,
                is_anomaly INTEGER NOT NULL DEFAULT 0,
                computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_classifications_region ON region_classifications(region, computed_at DESC);
        """)
        
        # 5. session_tokens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_tokens (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        
        # 6. api_cache (on-demand API response caching with TTL)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_cache (
                cache_key TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                response_json TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_api_cache_expires ON api_cache(expires_at);
        """)
        
        logger.info("Database schema initialized successfully.")

# --- Cache Helper Functions ---

def get_cached_api_response(cache_key: str) -> Optional[Any]:
    """Retrieves cached API response if not expired."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT response_json FROM api_cache WHERE cache_key = ? AND expires_at > ?",
                (cache_key, now)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row["response_json"])
    except Exception as e:
        logger.warning(f"Cache read error for key {cache_key}: {e}")
    return None

def set_cached_api_response(cache_key: str, source: str, data: Any, ttl_minutes: int = 30) -> None:
    """Stores API response in cache with TTL."""
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=ttl_minutes)
    data_str = json.dumps(data)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO api_cache (cache_key, source, response_json, expires_at, created_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    response_json = excluded.response_json,
                    expires_at = excluded.expires_at,
                    created_at = excluded.created_at
                """,
                (cache_key, source, data_str, expires.isoformat(), now.isoformat())
            )
    except Exception as e:
        logger.warning(f"Cache write error for key {cache_key}: {e}")

def record_gap_score(region: str, gap_score: float, media_volume: int, response_volume: int) -> None:
    """Appends a gap score snapshot to gap_score_cache."""
    now = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO gap_score_cache (region, gap_score, media_volume, response_volume, computed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (region, gap_score, media_volume, response_volume, now)
        )

def get_latest_gap_scores() -> list[dict]:
    """Retrieves the most recent gap score per region."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.region, g.gap_score, g.media_volume, g.response_volume, g.computed_at
            FROM gap_score_cache g
            INNER JOIN (
                SELECT region, MAX(computed_at) as max_computed
                FROM gap_score_cache
                GROUP BY region
            ) latest ON g.region = latest.region AND g.computed_at = latest.max_computed
            ORDER BY g.gap_score DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

# --- User & Watchlist Helper Functions ---

def create_user(email: str, password_hash: str) -> Dict[str, Any]:
    """Creates a new user record in SQLite."""
    user_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO users (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (user_id, email.lower().strip(), password_hash, now)
        )
    return {"id": user_id, "email": email.lower().strip(), "created_at": now}

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieves user row by email."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password_hash, created_at FROM users WHERE email = ?", (email.lower().strip(),))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves user row by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password_hash, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_watchlist(user_id: str) -> List[str]:
    """Retrieves list of bookmarked countries/crises for a user."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT country_or_crisis FROM watchlists WHERE user_id = ? ORDER BY added_at DESC",
            (user_id,)
        )
        return [row["country_or_crisis"] for row in cursor.fetchall()]

def add_to_watchlist(user_id: str, country_or_crisis: str) -> bool:
    """Adds a country or crisis to user's persistent watchlist if not already present."""
    entry_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM watchlists WHERE user_id = ? AND country_or_crisis = ?",
            (user_id, country_or_crisis)
        )
        if cursor.fetchone():
            return False
        cursor.execute(
            "INSERT INTO watchlists (id, user_id, country_or_crisis, added_at) VALUES (?, ?, ?, ?)",
            (entry_id, user_id, country_or_crisis, now)
        )
        return True

def remove_from_watchlist(user_id: str, country_or_crisis: str) -> bool:
    """Removes a country or crisis from user's watchlist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM watchlists WHERE user_id = ? AND country_or_crisis = ?",
            (user_id, country_or_crisis)
        )
        return cursor.rowcount > 0

def get_historical_gap_scores(region: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieves historical gap score snapshots for a region ordered by computed_at ASC."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT region, gap_score, media_volume, response_volume, computed_at
            FROM gap_score_cache
            WHERE region = ?
            ORDER BY computed_at ASC
            LIMIT ?
        """, (region, limit))
        return [dict(row) for row in cursor.fetchall()]
