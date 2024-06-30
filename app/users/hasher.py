from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
