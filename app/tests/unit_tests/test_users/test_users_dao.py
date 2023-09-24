import pytest
from pydantic import EmailStr

from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id,email,exists",
    [
        (1, "user1@user.com", True),
        (2, "user2@user.com", True),
        (101, "", False),
    ],
)
async def test_find_user_by_id(user_id: int, email: EmailStr, exists: bool):
    user = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert user is None


async def test_find_all_users():
    users = await UsersDAO.find_all()

    assert users[0]["email"] == "user1@user.com"
    assert users[1]["email"] == "user2@user.com"
