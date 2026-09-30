import httpx
import logging
import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.config import settings
from app.database import get_cached_api_response, set_cached_api_response
from app.models.schemas import GDELTArticle
from data.seeds.seed_data import GLOBAL_HOTSPOTS

logger = logging.getLogger(__name__)

class GDELTService:
    """Service layer for interacting with GDELT 2.0 Doc API with caching and 429 throttling mitigation."""

    def __init__(self):
        self.base_url = settings.GDELT_BASE_URL
        self.cache_ttl = settings.CACHE_TTL_MINUTES
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 CrisisPulse/1.0"
        }

    async def fetch_articles(
        self,
        query: str = "crisis",
        timespan: str = "24h",
        maxrecords: int = 50,
        country: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetches articles from GDELT 2.0 Doc API or cache."""
        cache_key = f"gdelt:{query}:{timespan}:{maxrecords}:{country or 'all'}"
        cached = get_cached_api_response(cache_key)
        if cached:
            logger.debug(f"Cache hit for GDELT query: {cache_key}")
            return {"source": "cache", "cached": True, "articles": cached}

        search_query = query
        if country:
            search_query = f"{country} ({query})"

        params = {
            "query": search_query,
            "mode": "artlist",
            "format": "json",
            "timespan": timespan,
            "maxrecords": str(min(maxrecords, 250))
        }

        articles_data: List[Dict[str, Any]] = []
        is_fallback = False

        try:
            async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS, follow_redirects=True) as client:
                response = await client.get(self.base_url, params=params, headers=self.headers)
                
                if response.status_code == 200:
                    try:
                        raw = response.json()
                        raw_articles = raw.get("articles", [])
                        for item in raw_articles:
                            articles_data.append(self._normalize_article(item, country))
                    except Exception as json_err:
                        logger.warning(f"Failed to parse GDELT JSON: {json_err}. Using fallback.")
                        is_fallback = True
                elif response.status_code == 429:
                    logger.warning("GDELT 429 Too Many Requests encountered. Using resilient regional fallback.")
                    is_fallback = True
                else:
                    logger.warning(f"GDELT returned HTTP {response.status_code}. Using fallback.")
                    is_fallback = True

        except Exception as exc:
            logger.warning(f"GDELT network request failed: {exc}. Using fallback.")
            is_fallback = True

        if is_fallback or not articles_data:
            articles_data = self._generate_fallback_articles(query, country)

        # Cache the result
        set_cached_api_response(cache_key, "gdelt", articles_data, ttl_minutes=self.cache_ttl)

        return {
            "source": "fallback" if is_fallback else "live",
            "cached": False,
            "articles": articles_data
        }

    def _normalize_article(self, raw: Dict[str, Any], country: Optional[str] = None) -> Dict[str, Any]:
        """Maps GDELT raw fields to standardized GDELTArticle schema."""
        # GDELT tone approximation from title sentiment if not in doc response
        title = raw.get("title", "Untitled Event")
        tone = self._estimate_tone_from_title(title)
        goldstein = round(tone * 1.2, 2)  # Scale to approximate Goldstein index [-10, 10]
        
        return {
            "url": raw.get("url", ""),
            "title": title,
            "seendate": raw.get("seendate", datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")),
            "domain": raw.get("domain", ""),
            "language": raw.get("language", "English"),
            "sourcecountry": raw.get("sourcecountry", country or "Unknown"),
            "socialimage": raw.get("socialimage"),
            "tone": tone,
            "goldstein": goldstein
        }

    def _estimate_tone_from_title(self, title: str) -> float:
        """Lightweight sentiment/tone heuristic for GDELT news events (-10.0 to +10.0)."""
        lower = title.lower()
        negative_keywords = [
            "kill", "attack", "dead", "shelling", "strike", "war", "famine", "disaster",
            "conflict", "bomb", "collapse", "death", "crisis", "hostage", "toll", "casualties",
            "escalat", "violat", "clash"
        ]
        positive_keywords = [
            "peace", "truce", "ceasefire", "aid", "agreement", "reconstruct", "safe", "relief",
            "cooperation", "deliver", "success", "support", "accord"
        ]
        
        neg_count = sum(1 for w in negative_keywords if w in lower)
        pos_count = sum(1 for w in positive_keywords if w in lower)
        
        if neg_count == 0 and pos_count == 0:
            return -1.5  # Neutral-leaning negative for typical international conflict monitoring
        
        base = (pos_count * 2.5) - (neg_count * 3.0)
        # Constrain to [-10, +10]
        return max(-10.0, min(10.0, round(base, 2)))

    def _generate_fallback_articles(self, query: str, country: Optional[str] = None) -> List[Dict[str, Any]]:
        """Provides realistic reference articles when GDELT is throttled or unreachable."""
        target_hotspots = GLOBAL_HOTSPOTS
        if country:
            matching = [h for h in GLOBAL_HOTSPOTS if h["region"].lower() == country.lower() or h["country_code"].lower() == country.lower()]
            if matching:
                target_hotspots = matching

        fallback_list = []
        now_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        
        for hotspot in target_hotspots:
            clean_region = hotspot["region"].split("(")[0].strip()
            for headline in hotspot["gdelt_sample_headlines"]:
                tone_val = round(random.uniform(*hotspot["tone_range"]), 2)
                encoded_query = f"{clean_region} {headline}".replace(" ", "+")
                fallback_list.append({
                    "url": f"https://news.google.com/search?q={encoded_query}",
                    "title": f"[{hotspot['region']}] {headline}",
                    "seendate": now_str,
                    "domain": "news.google.com",
                    "language": "English",
                    "sourcecountry": hotspot["country_code"],
                    "socialimage": None,
                    "tone": tone_val,
                    "goldstein": round(tone_val * 1.1, 2)
                })

        return fallback_list
