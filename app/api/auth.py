from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.schemas.user import UserCreate, UserRead
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