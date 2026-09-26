import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    PROJECT_NAME: str = "CrisisPulse"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Storage
    DATA_DIR: Path = BASE_DIR / "data"
    DATABASE_PATH: Path = BASE_DIR / "data" / "crisispulse.db"
    
    # External APIs
    GDELT_BASE_URL: str = "https://api.gdeltproject.org/api/v2/doc/doc"
    RELIEFWEB_BASE_URL: str = "https://api.reliefweb.int/v2"
    RELIEFWEB_APPNAME: str = os.getenv("RELIEFWEB_APPNAME", "crisis-pulse-tracker-app")
    
    # Rate limiting & caching
    CACHE_TTL_MINUTES: int = 30
    HTTP_TIMEOUT_SECONDS: float = 4.0
    GDELT_MIN_INTERVAL_SECONDS: float = 5.0
    
    # Security / Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "crisispulse-insecure-dev-secret-change-in-prod-12345678")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

settings = Settings()
