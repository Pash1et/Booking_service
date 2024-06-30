from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users import exceptions as ex
from app.users.auth import authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.hasher import Hasher
from app.users.shemas import SUserAuth, SUserShow

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register")
async def register_user(
    user_data: SUserAuth,
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    existing_user = await UserDAO.find_one_or_none(
        session=session, email=user_data.email
    )
    if existing_user:
        raise ex.UserAleadyExistException
    hashed_password = Hasher.get_password_hash(password=user_data.password)
    await UserDAO.add_one(
        session=session,
        email=user_data.email,
        hashed_password=hashed_password,
    )


@router.post("/login")
async def login_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: SUserAuth,
    response: Response,
) -> SUserShow:
    user = await authenticate_user(
        session, user_data.email, user_data.password
    )
    if not user:
        raise ex.NotFoundUserException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return user


@router.get("/me")
async def get_me(user: Annotated[str, Depends(get_current_user)]) -> SUserShow:
    return user


@router.post("/logout")
async def logut_user(response: Response):
    response.delete_cookie("access_token")
