from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    photo_id = Column(
        Integer,
        ForeignKey("photos.id", ondelete="CASCADE")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    content = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now()
    )

    photo = relationship(
        "Photo",
        back_populates="comments"
    )

    user = relationship(
        "User",
        back_populates="comments"
    )