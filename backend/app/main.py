import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api.routes import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("crisispulse")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup initialization and graceful shutdown."""
    logger.info(f"Starting {settings.PROJECT_NAME} backend v{settings.VERSION}...")
    init_db()
    logger.info("Database initialized and ready.")
    yield
    logger.info(f"Shutting down {settings.PROJECT_NAME} backend.")

app = FastAPI(
    title="CrisisPulse API",
    description="Global Conflict & Humanitarian Response Tracker fusing GDELT news monitoring and UN OCHA ReliefWeb tracking.",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "Global Conflict & Humanitarian Response Tracker",
        "documentation": "/docs",
        "health_check": f"{settings.API_PREFIX}/health",
        "aggregated_data": f"{settings.API_PREFIX}/data/aggregated"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
