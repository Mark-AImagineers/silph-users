from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base

class TokenBlacklist(Base):
    """Record of JWT tokens that have been invalidated."""

    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())

