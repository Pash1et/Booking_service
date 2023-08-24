from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.users import exceptions
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.shemas import SUserAuth
from app.users.utils import _get_expire
from app.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise exceptions.UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        email=user_data.email,
        hashed_password=hashed_password
    )


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await auth_user(
        email=user_data.email,
        password=user_data.password
    )
    if not user:
        raise exceptions.IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    expire = _get_expire(access_token)
    response.set_cookie(
        "booking_access_token",
        access_token,
        httponly=True,
        expires=expire.strftime("%a, %d %b %Y %H:%M:%S"),
        max_age=int(settings.EXPIRE) * 60
    )
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_user_me(
    current_user: Annotated[Users, Depends(get_current_user)]
):
    return current_user


@router.get("/all_users")
async def read_user_all(
    current_user: Annotated[Users, Depends(get_current_user)]
):
    return await UsersDAO.find_all()
