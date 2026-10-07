from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.data import router as data_router
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router, watchlist_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(data_router)
api_router.include_router(analytics_router)
api_router.include_router(auth_router)
api_router.include_router(watchlist_router)

