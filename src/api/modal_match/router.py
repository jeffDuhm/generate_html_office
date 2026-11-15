from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from corepy.modal_match.modal_match_exceptions import (
    InvalidModalMatchUpdateError,
    ModalMatchConflictError,
    ModalMatchNotFoundError,
    SiteNotFoundError,
)
from corepy.modal_match.modal_match_schemas import (
    CreateModalMatchSchema,
    UpdateModalMatchSchema,
)
from corepy.modal_match.modal_match_usecases import ModalMatchUsecases
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.user.user_dbs import UsersDB

router = APIRouter()

@router.get("/sites/{site_id}/modal-matches")
def get_all_by_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    result = ModalMatchUsecases(db).get_all_by_site(site_id, current_user.id)
    return result

@router.post("/sites/{site_id}/modal-matches")
def create(
    site_id: int,
    new_match: CreateModalMatchSchema,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result = ModalMatchUsecases(db).create(site_id, current_user.id, new_match)
        return result
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )

@router.patch("/modal-matches/{match_id}")
def update(
    match_id: int,
    match_update: UpdateModalMatchSchema,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result = ModalMatchUsecases(db).update(match_id, current_user.id, match_update)
        return result
    except ModalMatchNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except InvalidModalMatchUpdateError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response_error.model_dump(),
        )
    except ModalMatchConflictError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.delete("/modal-matches/{match_id}")
def delete(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result = ModalMatchUsecases(db).delete(match_id, current_user.id)
        return result
    except ModalMatchNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except ModalMatchConflictError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )