from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)

    photo_id = Column(
        Integer,
        ForeignKey("photos.id", ondelete="CASCADE")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    rating = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "photo_id",
            "user_id",
            name="uq_rating"
        ),
    )

    photo = relationship(
        "Photo",
        back_populates="ratings"
    )

    user = relationship(
        "User",
        back_populates="ratings"
    )