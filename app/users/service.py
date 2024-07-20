from uuid import UUID
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.tasks import send_user_confirm_code
from app.users.auth import authenticate_user, create_access_token
from app.users.dao import UserConfirmCodeDAO, UserDAO
from app.users.hasher import Hasher
from app.users.shemas import SUserAuth
from app.users import exceptions as ex


class UserService:
    @classmethod
    async def register_user(cls, session: AsyncSession, user_data: SUserAuth):
        existing_user = await UserDAO.find_one_or_none(
            session=session, email=user_data.email
        )
        if existing_user:
            raise ex.UserAleadyExistException
        hashed_password = Hasher.get_password_hash(user_data.password)
        user = await UserDAO.add_one(
            session=session,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        code = await UserConfirmCodeDAO.create_confirm_code(session, user)
        send_user_confirm_code.delay(user.email, code.code)
        return user

    @classmethod
    async def login_user(
        cls, session: AsyncSession, user_data: SUserAuth, response: Response
    ):
        user = await authenticate_user(
            session, user_data.email, user_data.password
        )
        if not user:
            raise ex.NotFoundUserException
        if not user.is_active:
            raise ex.UserIsNotActiavate
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie(
            key="access_token", value=access_token, httponly=True
        )
        return user

    @classmethod
    async def user_confirm_account(cls, session: AsyncSession, code: UUID):
        check_code = await UserConfirmCodeDAO.find_one_or_none(session, code=code)
        if not check_code:
            raise ex.UserConfirmationCodeNotFound
        await UserDAO.update_one(session, check_code.user_id, is_active=True)
        await UserConfirmCodeDAO.delete_one(session, check_code.id)
        return {"detail": "Аккаунт активирован."}
