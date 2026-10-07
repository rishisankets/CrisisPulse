import re
import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status, Depends

from app.models.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    AuthResponse,
    WatchlistAddRequest,
    WatchlistResponse,
)
from app.database import (
    create_user,
    get_user_by_email,
    get_user_watchlist,
    add_to_watchlist,
    remove_from_watchlist,
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_optional_user,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication & Watchlists"])
watchlist_router = APIRouter(prefix="/watchlists", tags=["Watchlists"])

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

@router.post("/register", response_model=AuthResponse)
async def register(req: UserRegisterRequest):
    """Registers a new user with email and password, returning JWT token."""
    clean_email = req.email.strip().lower()
    if not re.match(EMAIL_REGEX, clean_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    if len(req.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    existing = get_user_by_email(clean_email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    pw_hash = hash_password(req.password)
    user = create_user(clean_email, pw_hash)
    token = create_access_token(user_id=user["id"], email=user["email"])
    
    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            created_at=user.get("created_at")
        )
    )

@router.post("/login", response_model=AuthResponse)
async def login(req: UserLoginRequest):
    """Authenticates user with email and password, returning JWT token."""
    clean_email = req.email.strip().lower()
    user = get_user_by_email(clean_email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = create_access_token(user_id=user["id"], email=user["email"])
    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            created_at=user.get("created_at")
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    """Returns currently authenticated user profile."""
    return UserResponse(
        id=user["id"],
        email=user["email"],
        created_at=user.get("created_at")
    )

# --- Watchlists ---

@watchlist_router.get("", response_model=WatchlistResponse)
async def get_watchlist(user: Dict[str, Any] = Depends(get_current_user)):
    """Fetches list of bookmarked crises for the authenticated user."""
    items = get_user_watchlist(user["id"])
    return WatchlistResponse(items=items)

@watchlist_router.post("", response_model=WatchlistResponse)
async def add_watchlist_item(
    req: WatchlistAddRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Adds a crisis region to the authenticated user's persistent watchlist."""
    add_to_watchlist(user["id"], req.country_or_crisis.strip())
    items = get_user_watchlist(user["id"])
    return WatchlistResponse(items=items)

@watchlist_router.delete("/{region}", response_model=WatchlistResponse)
async def remove_watchlist_item(
    region: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Removes a crisis region from the authenticated user's watchlist."""
    remove_from_watchlist(user["id"], region.strip())
    items = get_user_watchlist(user["id"])
    return WatchlistResponse(items=items)
