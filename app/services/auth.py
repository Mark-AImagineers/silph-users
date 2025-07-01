from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.token import TokenPair
from app.core.security import hash_password, verify_password
from app.core.token import (
    create_access_token,
    create_refresh_token,
    ALGORITHM,
)
from app.services.token_blacklist import TokenBlacklistService
from app.core.config import settings
from jose import jwt, JWTError
from sqlalchemy.exc import IntegrityError

class AuthService:
    @staticmethod
    async def register(data: UserCreate, db: AsyncSession) -> User:
        # Check if email or username already exists
        result = await db.execute(
            select(User).where((User.email == data.email) | (User.username == data.username))
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError("Email or username already taken")
        
        # Hash Password and Create User
        new_user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
        )
        db.add(new_user)
        try:
            await db.commit()
            await db.refresh(new_user)
            return new_user
        except IntegrityError:
            await db.rollback()
            raise ValueError("Failed to create user - possible duplicate entry")
    
    @staticmethod
    async def authenticate(email: str, password: str, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def refresh(refresh_token: str, db: AsyncSession) -> TokenPair:
        """Return new JWT tokens using the provided refresh token."""
        try:
            payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[ALGORITHM])
            user_id: str | None = payload.get("sub")
            jti: str | None = payload.get("jti")
            if user_id is None or jti is None:
                raise JWTError()
        except JWTError as exc:
            raise ValueError("Invalid refresh token") from exc

        if await TokenBlacklistService.is_blacklisted(jti, db):
            raise ValueError("Invalid refresh token")

        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        if user is None:
            raise ValueError("User not found")

        await TokenBlacklistService.blacklist(jti, db)

        claims = {"sub": str(user.id), "email": user.email}
        return TokenPair(
            access_token=create_access_token(claims),
            refresh_token=create_refresh_token(claims),
        )
