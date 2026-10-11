from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.user.user_exceptions import CannotDeleteSelfError, RepeatedEmailError, UserInUseError, UserNotFoundError
from corepy.user.user_schemas import CreateUserSchema, UpdateUserSchema
from corepy.user.user_usecases import UserUsecases

router = APIRouter()

@router.get("")
def get_all():
    result_users = UserUsecases().get_all()
    return result_users

@router.get("/{user_id}")
def get_by_id(user_id: int):
    try:
        result_user = UserUsecases().get_by_id(user_id)
        return result_user
    except UserNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )

@router.post("", status_code=status.HTTP_201_CREATED)
def create(new_user: CreateUserSchema):
    try:
        result_user = UserUsecases().create(new_user)
        return result_user
    except RepeatedEmailError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.patch("/{user_id}")
def update(user_id: int, user: UpdateUserSchema):
    try:
        result_user = UserUsecases().update(user_id, user)
        return result_user
    except UserNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except RepeatedEmailError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.delete("/{user_id}")
def delete(user_id: int):
    try:
        result_user = UserUsecases().delete(user_id)
        return result_user
    except UserNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except (CannotDeleteSelfError, UserInUseError) as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )