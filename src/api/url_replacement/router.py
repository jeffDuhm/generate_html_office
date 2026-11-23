from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.url_replacement.url_replacement_exceptions import (
    InvalidUrlReplacementUpdateError,
    UrlReplacementAlreadyExistsError,
    UrlReplacementDeleteError,
    UrlReplacementNotFoundError,
)
from corepy.url_replacement.url_replacement_schemas import (
    CreateUrlReplacementSchema,
    UpdateUrlReplacementSchema,
)
from corepy.url_replacement.url_replacement_usecases import UrlReplacementUsecases
from corepy.user.user_dbs import UsersDB

router = APIRouter()

@router.get("/sites/{site_id}/url-replacements")
def get_url_replacements(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_replacements = UrlReplacementUsecases(db).get_all_by_site(user_id=current_user.id, site_id=site_id)
        return result_replacements
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
        

@router.post("/sites/{site_id}/url-replacements")
def create_url_replacement(
    site_id: int,
    new_replacement: CreateUrlReplacementSchema,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_replacement = UrlReplacementUsecases(db).create(
            user_id=current_user.id,
            site_id=site_id,
            new_replacement=new_replacement,
        )
        return result_replacement
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except UrlReplacementAlreadyExistsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.patch("/url-replacements/{url_replacement_id}")
def update_url_replacement(
    url_replacement_id: int,
    url_replacement_update: UpdateUrlReplacementSchema,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_replacement = UrlReplacementUsecases(db).update(
            user_id=current_user.id,
            url_replacement_id=url_replacement_id,
            url_replacement_update=url_replacement_update,
        )
        return result_replacement
    
    except UrlReplacementNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except InvalidUrlReplacementUpdateError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_error.model_dump(),
        )
    except UrlReplacementAlreadyExistsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )

@router.delete("/url-replacements/{url_replacement_id}")
def delete_url_replacement(
    url_replacement_id: int,
    db: Session = Depends(get_db),
    current_user: UsersDB = Depends(get_current_user),
):
    try:
        result_replacement = UrlReplacementUsecases(db).delete(
            user_id=current_user.id,
            url_replacement_id=url_replacement_id,
        )
        return result_replacement
    except UrlReplacementNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except UrlReplacementDeleteError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )