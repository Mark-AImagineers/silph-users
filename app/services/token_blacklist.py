from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.token_blacklist import TokenBlacklist

class TokenBlacklistService:
    """Service for managing blacklisted JWT tokens."""

    @staticmethod
    async def is_blacklisted(jti: str, db: AsyncSession) -> bool:
        """Check whether a token has been blacklisted."""
        result = await db.execute(select(TokenBlacklist).where(TokenBlacklist.jti == jti))
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def blacklist(jti: str, db: AsyncSession) -> None:
        """Add a token's JTI to the blacklist."""
        db.add(TokenBlacklist(jti=jti))
        await db.commit()

