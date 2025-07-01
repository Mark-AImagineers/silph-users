import os
import sys
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from jose import jwt

sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('JWT_SECRET', 'test-secret')
from app.models.base import Base
from app.models.user import User
from app.services.auth import AuthService
from app.services.token_blacklist import TokenBlacklistService
from app.core.token import create_refresh_token, ALGORITHM

@pytest.mark.asyncio
async def test_refresh_blacklists_token():
    os.environ['JWT_SECRET'] = 'test-secret'
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as db:
        user = User(email='x@example.com', username='x', hashed_password='y')
        db.add(user)
        await db.commit()
        await db.refresh(user)
        claims = {'sub': str(user.id), 'email': user.email}
        refresh_token = create_refresh_token(claims)
        tokens = await AuthService.refresh(refresh_token, db)
        payload = jwt.decode(refresh_token, 'test-secret', algorithms=[ALGORITHM])
        assert await TokenBlacklistService.is_blacklisted(payload['jti'], db)
        with pytest.raises(ValueError):
            await AuthService.refresh(refresh_token, db)

