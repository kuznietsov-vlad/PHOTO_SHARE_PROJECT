from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from models.photo_tags import photo_tags


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    cloudinary_public_id = Column(
        String(255),
        unique=True,
        nullable=False
    )

    cloudinary_url = Column(
        Text,
        nullable=False
    )

    description = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now()
    )

    owner = relationship(
        "User",
        back_populates="photos"
    )

    tags = relationship(
        "Tag",
        secondary=photo_tags,
        back_populates="photos"
    )

    comments = relationship(
        "Comment",
        back_populates="photo",
        cascade="all, delete"
    )

    ratings = relationship(
        "Rating",
        back_populates="photo",
        cascade="all, delete"
    )

    transformed_images = relationship(
        "TransformedImage",
        back_populates="photo",
        cascade="all, delete"
    )