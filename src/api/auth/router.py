from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from corepy.auth.auth_usecases import AuthUsecases
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import (
    ResponseErrorSchema,
    ResponseSuccessSchema,
)
from corepy.user.user_dbs import UsersDB
from corepy.user.user_exceptions import InvalidCredentialsError
from corepy.user.user_messages import SuccessUserMessages
from corepy.user.user_schemas import UserAuthSchema, UserSchema

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        credentials = UserAuthSchema(email=form_data.username, password=form_data.password)
        return AuthUsecases(db).login(credentials)
    except InvalidCredentialsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response_error.model_dump()
        )

@router.get("/me")
def me(current_user: UsersDB = Depends(get_current_user)):
    user = UserSchema.model_validate(current_user)
    return ResponseSuccessSchema(
        message=SuccessUserMessages.USER_GET,
        data=user
    )