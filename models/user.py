from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="user")

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    photos = relationship(
        "Photo",
        back_populates="owner",
        cascade="all, delete"
    )

    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete"
    )

    ratings = relationship(
        "Rating",
        back_populates="user",
        cascade="all, delete"
    )