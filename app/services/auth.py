from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
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