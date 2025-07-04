from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import TokenPair
from app.core.token import create_access_token, create_refresh_token, get_current_user
from app.services.auth import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await AuthService.register(data, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/login", response_model=TokenPair)
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await AuthService.authenticate(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    claims = {"sub": str(user.id), "email": user.email}

    return TokenPair(
        access_token=create_access_token(claims),
        refresh_token=create_refresh_token(claims),
    )

@router.post("/refresh", response_model=TokenPair)
async def refresh(
    refresh_token: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """Generate new tokens using a valid refresh token."""
    try:
        return await AuthService.refresh(refresh_token, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user