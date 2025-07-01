from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import TokenPair
from app.core.token import create_access_token, create_refresh_token
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

async def get_db() -> AsyncSession: # type: ignore
    async with async_session() as session:
        yield session

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
