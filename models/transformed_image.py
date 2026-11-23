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


class TransformedImage(Base):
    __tablename__ = "transformed_images"

    id = Column(Integer, primary_key=True)

    photo_id = Column(
        Integer,
        ForeignKey("photos.id", ondelete="CASCADE")
    )

    transformation_name = Column(
        String(100),
        nullable=False
    )

    transformed_url = Column(
        Text,
        nullable=False
    )

    qr_code_url = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    photo = relationship(
        "Photo",
        back_populates="transformed_images"
    )