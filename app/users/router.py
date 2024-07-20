from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users.dependencies import get_current_user
from app.users.service import UserService
from app.users.shemas import SUserAuth, SUserShow

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: SUserAuth,
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> SUserShow:
    return await UserService.register_user(session, user_data)


@router.post("/confirm_code", status_code=status.HTTP_200_OK)
async def user_confirm_account(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    code: UUID,
):
    return await UserService.user_confirm_account(session, code)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: SUserAuth,
    response: Response,
) -> SUserShow:
    return await UserService.login_user(session, user_data, response)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(user: Annotated[str, Depends(get_current_user)]) -> SUserShow:
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logut_user(response: Response):
    response.delete_cookie("access_token")
