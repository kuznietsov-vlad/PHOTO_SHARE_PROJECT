from database import Base, engine

from models.user import User
from models.photo import Photo
from models.tag import Tag
from models.comment import Comment
from models.rating import Rating
from models.transformed_image import TransformedImage
from models.token_blacklist import TokenBlacklist

Base.metadata.create_all(bind=engine)

print("Tables created")