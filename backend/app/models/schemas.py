from typing import Optional, List, Dict, Any
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field

class GDELTArticle(BaseModel):
    url: str
    title: str
    seendate: str
    domain: Optional[str] = None
    language: Optional[str] = "English"
    sourcecountry: Optional[str] = None
    socialimage: Optional[str] = None
    tone: Optional[float] = 0.0
    goldstein: Optional[float] = 0.0

class ReliefWebReport(BaseModel):
    id: str
    title: str
    date: Optional[str] = None
    primary_country: Optional[str] = None
    country_code: Optional[str] = None
    source: Optional[str] = None
    format: Optional[str] = "Situation Report"
    url: Optional[str] = None
    body_snippet: Optional[str] = None

class RegionFeatureVector(BaseModel):
    region: str
    country_code: str
    lat: float
    lon: float
    event_volume_24h: int = Field(description="GDELT event count in last 24h")
    event_volume_7d: int = Field(description="GDELT event count in last 7d")
    volume_ratio: float = Field(description="24h volume vs 7d daily baseline ratio")
    avg_goldstein: float = Field(description="Average conflict/cooperation intensity [-10.0 to +10.0]")
    goldstein_trend: float = Field(description="24h tone delta vs baseline")
    tone_volatility: float = Field(description="Standard deviation of event sentiment")
    reliefweb_response_count: int = Field(description="ReliefWeb active appeals and reports in window")
    computed_at: str

class AggregatedDataResponse(BaseModel):
    total_regions: int
    data_sources: Dict[str, str]
    cached: bool
    features: List[RegionFeatureVector]

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    gdelt_status: str
    reliefweb_status: str
    timestamp: str

class RegionAnalyticsItem(BaseModel):
    region: str
    country_code: str
    lat: float
    lon: float
    gap_score: float = Field(description="Attention-response disparity score from 0.0 to 10.0")
    category: str = Field(description="Archetype: Neglected Emergency, Escalating Hotspot, Protracted Crisis, Stabilized Response")
    is_anomaly: bool = Field(description="Isolation forest anomaly detection outlier flag")
    media_volume_24h: int
    reliefweb_response_count: int
    volume_ratio: float
    avg_goldstein: float
    tone_volatility: float
    computed_at: str

class AnalyticsOverviewResponse(BaseModel):
    timestamp: str
    total_analyzed: int
    neglected_count: int
    escalating_count: int
    anomalies_detected: int
    results: List[RegionAnalyticsItem]

class GapScoreRankingItem(BaseModel):
    region: str
    gap_score: float
    media_volume: int
    response_volume: int
    computed_at: str

# Auth Schemas
class UserRegisterRequest(BaseModel):
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: Optional[str] = None

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

class WatchlistAddRequest(BaseModel):
    country_or_crisis: str

class WatchlistResponse(BaseModel):
    items: List[str]

