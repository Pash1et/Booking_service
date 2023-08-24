from datetime import datetime

from jose import jwt

from app.config import settings


def _get_expire(access_token):
    payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    expire_timestamp = payload.get("exp")
    expire = datetime.fromtimestamp(expire_timestamp)
    return expire
