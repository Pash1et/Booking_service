import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import EmailStr


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("user@user.com", "UserPassword", status.HTTP_200_OK),
        ("user1@user.com", "UserPassword", status.HTTP_401_UNAUTHORIZED),
        ("qwerty", "password", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("", "UserPassword", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_register_user(
    email: EmailStr,
    password: str,
    status_code: status,
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("user1@user.com", "user1password", status.HTTP_200_OK),
        ("user2@user.com", "user2password", status.HTTP_200_OK),
        ("unknown@user.com", "userpassword", status.HTTP_401_UNAUTHORIZED),
        ("", "userpassword", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_login_user(
    email: EmailStr,
    password: str,
    status_code: status,
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
    assert async_client.cookies["booking_access_token"]


async def test_logout_user(async_client: AsyncClient):
    response = await async_client.post("/auth/logout")

    assert response.status_code == status.HTTP_200_OK
    assert "booking_access_token" not in async_client.cookies
