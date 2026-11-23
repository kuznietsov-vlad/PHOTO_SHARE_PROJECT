from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import RoleEnum, User
from src.repository import users as repo_users
from src.schemas.auth import (
    MessageSchema,
    RefreshTokenRequest,
    TokenSchema,
    UserResponseSchema,
    UserSignupSchema,
)
from src.services.auth import auth_service, get_current_user, oauth2_scheme

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/signup",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Реєстрація нового користувача (перший користувач стає admin)",
)
def signup(body: UserSignupSchema, db: Session = Depends(get_db)):
    if repo_users.get_user_by_email(body.email, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists",
        )
    if repo_users.get_user_by_username(body.username, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this username already exists",
        )

    role = RoleEnum.admin if repo_users.count_users(db) == 0 else RoleEnum.user
    hashed_password = auth_service.get_password_hash(body.password)
    return repo_users.create_user(body, hashed_password, role, db)


@router.post(
    "/login",
    response_model=TokenSchema,
    summary="Вхід користувача та отримання JWT-токенів",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = repo_users.get_user_by_username(form_data.username, db)
    if user is None:
        user = repo_users.get_user_by_email(form_data.username, db)

    if user is None or not auth_service.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    token_data = {"sub": user.email, "role": user.role.value}
    access_token = auth_service.create_access_token(data=token_data)
    refresh_token = auth_service.create_refresh_token(data=token_data)
    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh",
    response_model=TokenSchema,
    summary="Оновлення access та refresh токенів",
)
def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    email = auth_service.decode_refresh_token(body.refresh_token)
    user = repo_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    token_data = {"sub": user.email, "role": user.role.value}
    new_access = auth_service.create_access_token(data=token_data)
    new_refresh = auth_service.create_refresh_token(data=token_data)
    return TokenSchema(access_token=new_access, refresh_token=new_refresh)


@router.post(
    "/logout",
    response_model=MessageSchema,
    summary="Вихід із системи (додає поточний access-токен у чорний список)",
)
def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    payload = auth_service.decode_token(token)
    exp_timestamp = payload.get("exp")
    expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    repo_users.add_token_to_blacklist(token, expires_at, db)
    return MessageSchema(message=f"User '{current_user.username}' successfully logged out")