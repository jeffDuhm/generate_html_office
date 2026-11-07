from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.user.user_dbs import UsersDB
from corepy.widget_match.widget_match_exceptions import (
    InvalidWidgetMatchUpdateError,
    WidgetMatchConflictError,
    WidgetMatchNotFoundError,
    WidgetNotFoundError,
)
from corepy.widget_match.widget_match_schemas import (
    CreateWidgetMatchSchema,
    UpdateWidgetMatchSchema,
)
from corepy.widget_match.widget_match_usecases import WidgetMatchUsecases

router = APIRouter()

@router.get("/sites/{site_id}/config")
def get_all_by_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    result_matches = WidgetMatchUsecases(db).get_all_by_site(site_id, current_user.id)
    return result_matches

@router.post("/widgets/{widget_id}/matches")
def create(
    widget_id: int,
    new_match: CreateWidgetMatchSchema,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_match = WidgetMatchUsecases(db).create(
            widget_id, current_user.id, new_match
        )
        return result_match
    except WidgetNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except WidgetMatchConflictError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.patch("/widget-matches/{match_id}")
def update(
    match_id: int,
    match: UpdateWidgetMatchSchema,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_match = WidgetMatchUsecases(db).update(
            match_id, current_user.id, match
        )
        return result_match
    except WidgetMatchNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except InvalidWidgetMatchUpdateError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_error.model_dump(),
        )
    except WidgetMatchConflictError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.delete("/widget-matches/{match_id}")
def delete(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_match = WidgetMatchUsecases(db).delete(match_id, current_user.id)
        return result_match
    except WidgetMatchNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )