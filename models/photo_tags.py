from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

photo_tags = Table(
    "photo_tags",
    Base.metadata,
    Column(
        "photo_id",
        Integer,
        ForeignKey("photos.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)