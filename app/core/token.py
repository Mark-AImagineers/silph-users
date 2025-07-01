from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.auth import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db),) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user