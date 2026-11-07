import os
from datetime import datetime, timedelta, timezone
import jwt
from corepy.user.user_exceptions import ExpiredToken, InvalidToken

ALGORITHM = "HS256"
EXPIRE_HOURS = 8

def create_access_token(user_id: int) -> str:
    secret_key = os.environ["SECRET_KEY"]
    expire = datetime.now(timezone.utc) + timedelta(hours=EXPIRE_HOURS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str) -> int:
    secret_key = os.environ["SECRET_KEY"]
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise ExpiredToken()
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise InvalidToken()