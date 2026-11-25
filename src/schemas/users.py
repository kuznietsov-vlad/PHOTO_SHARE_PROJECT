from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.database.models import RoleEnum


class UserPublicProfileSchema(BaseModel):
    username: str
    full_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    role: RoleEnum
    created_at: datetime
    photos_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class UserMeSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    role: RoleEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime
    photos_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class UserUpdateMeSchema(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    full_name: str | None = Field(default=None, max_length=100)
    bio: str | None = Field(default=None, max_length=500)
    avatar_url: str | None = Field(default=None, max_length=512)


class UserStatusUpdateSchema(BaseModel):
    is_active: bool


class UserRoleUpdateSchema(BaseModel):
    role: RoleEnum