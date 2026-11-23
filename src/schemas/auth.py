from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.database.models import RoleEnum


class UserSignupSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    full_name: str | None = Field(default=None, max_length=100)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class MessageSchema(BaseModel):
    message: str