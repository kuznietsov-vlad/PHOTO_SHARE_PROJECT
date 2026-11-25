from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.database.models import BlacklistedToken, Photo, RoleEnum, User
from src.schemas.auth import UserSignupSchema
from src.schemas.users import UserUpdateMeSchema


def get_user_by_email(email: str, db: Session) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_user_by_username(username: str, db: Session) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))


def count_users(db: Session) -> int:
    return db.scalar(select(func.count(User.id))) or 0


def count_user_photos(user_id: int, db: Session) -> int:
    return db.scalar(select(func.count(Photo.id)).where(Photo.user_id == user_id)) or 0


def create_user(
    body: UserSignupSchema,
    hashed_password: str,
    role: RoleEnum,
    db: Session,
) -> User:
    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hashed_password,
        full_name=body.full_name,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_profile(
    user: User,
    body: UserUpdateMeSchema,
    db: Session,
) -> User:
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def update_user_status(user: User, is_active: bool, db: Session) -> User:
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


def update_user_role(user: User, role: RoleEnum, db: Session) -> User:
    user.role = role
    db.commit()
    db.refresh(user)
    return user


def add_token_to_blacklist(
    token: str,
    expires_at: datetime,
    db: Session,
) -> BlacklistedToken:
    blacklisted = BlacklistedToken(token=token, expires_at=expires_at)
    db.add(blacklisted)
    db.commit()
    db.refresh(blacklisted)
    return blacklisted


def is_token_blacklisted(token: str, db: Session) -> bool:
    existing = db.scalar(
        select(BlacklistedToken).where(BlacklistedToken.token == token)
    )
    return existing is not None