from jose import jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.users.auth import auth_user, create_access_token
from app.users.dependencies import get_current_user

from fastapi import status


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await auth_user(email, password)
        if user:
            access_token = create_access_token(
                {
                    "sub": str(user.id),
                    "email": email
                }
            )
            if jwt.decode(
                access_token,
                settings.SECRET_KEY,
                settings.ALGORITHM
            )["role"] == settings.ADMIN:
                request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=status.HTTP_302_FOUND
            )

        user = get_current_user(token)
        if not user:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=status.HTTP_302_FOUND
            )


authentication_backend = AdminAuth(secret_key="...")
