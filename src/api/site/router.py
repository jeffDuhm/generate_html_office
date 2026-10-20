from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, require_admin
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.site.site_exceptions import (
    SiteHasRelatedRecordsError,
    SiteInvalidUpdateError,
    SiteNameAlreadyExistsError,
    SiteNotFoundError,
)
from corepy.site.site_schemas import CreateSiteSchema, UpdateSiteSchema
from corepy.site.site_usecases import SiteUsecases

router = APIRouter(dependencies=[Depends(require_admin)])

user_router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("")
def get_all(db: Session = Depends(get_db)):
    result_sites = SiteUsecases(db).get_all()
    return result_sites


@router.get("/{site_id}")
def get_by_id(site_id: int, db: Session = Depends(get_db)):
    try:
        result_site = SiteUsecases(db).get_by_id(site_id)
        return result_site
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )


@router.post("", status_code=status.HTTP_201_CREATED)
def create(new_site: CreateSiteSchema, db: Session = Depends(get_db)):
    try:
        result_site = SiteUsecases(db).create(new_site)
        return result_site
    except SiteNameAlreadyExistsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )


@router.patch("/{site_id}")
def update(site_id: int, site: UpdateSiteSchema, db: Session = Depends(get_db)):
    try:
        result_site = SiteUsecases(db).update(site_id, site)
        return result_site
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except SiteNameAlreadyExistsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )
    except SiteInvalidUpdateError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_error.model_dump(),
        )


@router.delete("/{site_id}")
def delete(site_id: int, db: Session = Depends(get_db)):
    try:
        result_site = SiteUsecases(db).delete(site_id)
        return result_site
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )
    except SiteHasRelatedRecordsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump(),
        )


@user_router.get("")
def get_all_active(db: Session = Depends(get_db)):
    result_sites = SiteUsecases(db).get_all_active()
    return result_sites