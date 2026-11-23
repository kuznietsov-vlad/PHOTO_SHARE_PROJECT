from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from database import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)

    jti = Column(
        String(255),
        unique=True,
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )