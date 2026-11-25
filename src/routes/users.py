from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import RoleEnum, User
from src.repository import users as repo_users
from src.schemas.users import (
    UserMeSchema,
    UserPublicProfileSchema,
    UserRoleUpdateSchema,
    UserStatusUpdateSchema,
    UserUpdateMeSchema,
)
from src.services.auth import RoleChecker, get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])
admin_only = RoleChecker([RoleEnum.admin])


def _build_me_response(user: User, db: Session) -> UserMeSchema:
    photos_count = repo_users.count_user_photos(user.id, db)
    return UserMeSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        photos_count=photos_count,
    )


@router.get(
    "/me",
    response_model=UserMeSchema,
    summary="Перегляд власної інформації авторизованим користувачем",
)
def read_own_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _build_me_response(current_user, db)


@router.put(
    "/me",
    response_model=UserMeSchema,
    summary="Редагування власної інформації авторизованим користувачем",
)
def update_own_profile(
    body: UserUpdateMeSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.username and body.username != current_user.username:
        existing = repo_users.get_user_by_username(body.username, db)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Account with this username already exists",
            )

    updated_user = repo_users.update_user_profile(current_user, body, db)
    return _build_me_response(updated_user, db)


@router.get(
    "/profile/{username}",
    response_model=UserPublicProfileSchema,
    summary="Публічний профіль користувача за унікальним username",
)
def read_public_profile(username: str, db: Session = Depends(get_db)):
    user = repo_users.get_user_by_username(username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    photos_count = repo_users.count_user_photos(user.id, db)
    return UserPublicProfileSchema(
        username=user.username,
        full_name=user.full_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        role=user.role,
        created_at=user.created_at,
        photos_count=photos_count,
    )


@router.patch(
    "/{user_id}/status",
    response_model=UserMeSchema,
    summary="Бан або розбан користувача (лише для admin)",
)
def set_user_active_status(
    user_id: int,
    body: UserStatusUpdateSchema,
    current_admin: User = Depends(admin_only),
    db: Session = Depends(get_db),
):
    user = repo_users.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.id == current_admin.id and not body.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot ban themselves",
        )

    updated_user = repo_users.update_user_status(user, body.is_active, db)
    return _build_me_response(updated_user, db)


@router.patch(
    "/{user_id}/role",
    response_model=UserMeSchema,
    summary="Зміна ролі користувача (лише для admin)",
)
def set_user_role(
    user_id: int,
    body: UserRoleUpdateSchema,
    current_admin: User = Depends(admin_only),
    db: Session = Depends(get_db),
):
    user = repo_users.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.id == current_admin.id and body.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot remove their own admin role",
        )

    updated_user = repo_users.update_user_role(user, body.role, db)
    return _build_me_response(updated_user, db)