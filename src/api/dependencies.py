from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from corepy.auth.auth_tokens import decode_access_token
from corepy.user.user_dbs import UsersDB
from corepy.user.user_exceptions import (
    ExpiredToken,
    InvalidToken,
    InactiveUserError,
)
from corepy.user.user_queries import UserQueries
from corepy.shared.mysql.base import get_db

aouth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(aouth2_scheme), db: Session = Depends(get_db)) -> UsersDB:
    try:
        user_id = decode_access_token(token)
    except (InvalidToken, ExpiredToken) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    db_user = UserQueries(db).get_by_id(user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_UNAUTHORIZED,
            detail=str(InvalidToken()),
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(InactiveUserError())
        )
    return db_user

def require_admin(current_user: UsersDB = Depends(get_current_user)) -> UsersDB:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permissions required."
        )