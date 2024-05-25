from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_settings
from db.db import get_session
from schemas.user import AccessToken, User, UserCreate, UserLogin
from services.user import user_crud
from core.auth import create_access_token, hash_password, authenticate_user

user_router = APIRouter()


@user_router.post(
    '/register', response_model=User, status_code=status.HTTP_201_CREATED
)
async def register(
        *,
        db: AsyncSession = Depends(get_session),
        obj: UserCreate,
) -> Any:
    """
    Регистрация пользователя
    """
    obj.password = hash_password(obj.password)
    user = await user_crud.create(db=db, obj=obj)
    return user


@user_router.post(
    '/auth', response_model=AccessToken, status_code=status.HTTP_200_OK
)
async def auth(
        *,
        db: AsyncSession = Depends(get_session),
        obj: UserLogin,
) -> Any:
    """
    Авторизация пользователя
    """

    user = await authenticate_user(db, obj.login, obj.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=app_settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return AccessToken(access_token=access_token, token_type="bearer")
