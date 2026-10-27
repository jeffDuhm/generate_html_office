from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependencies import require_admin
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.widget.widget_exceptions import (
    WidgetHasRelatedRecordsError,
    WidgetInvalidUpdateError,
    WidgetNotFoundError,
    WidgetShortcodeAlreadyExistsError,
)
from corepy.widget.widget_schemas import CreateWidgetSchema, UpdateWidgetSchema
from corepy.widget.widget_usecases import WidgetUsecases


router = APIRouter(dependencies=[Depends(require_admin)])

@router.get("")
def get_all_by_site(site_id: int, db: Session = Depends(get_db)):
    try:
        result_widgets = WidgetUsecases(db).get_all_by_site(site_id)
        return result_widgets
    except WidgetNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump()
        )

@router.get("/{widget_id}")
def get_by_id(widget_id: int, site_id: int, db: Session = Depends(get_db)):
    try:
        result_widget = WidgetUsecases(db).get_by_id(widget_id, site_id)
        return result_widget
    except (WidgetNotFoundError, SiteNotFoundError) as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump()
        )
        
@router.post("", status_code=status.HTTP_201_CREATED)
def create(site_id: int, new_widget: CreateWidgetSchema, db: Session = Depends(get_db)):
    try:
        result_widget = WidgetUsecases(db).create(site_id, new_widget)
        return result_widget
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump()
        )
    except WidgetShortcodeAlreadyExistsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump()
        )
        
@router.patch("/{widget_id}")
def update(site_id: int, widget_id: int, widget: UpdateWidgetSchema, db: Session = Depends(get_db)):
    try:
        result_widget = WidgetUsecases(db).update(site_id, widget_id, widget)
        return result_widget
    except (SiteNotFoundError, WidgetNotFoundError) as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump()
        )
    except WidgetShortcodeAlreadyExistsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump()
        )
    except WidgetInvalidUpdateError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_error.model_dump()
        )
        
@router.delete("/{widget_id}")
def delete(site_id: int, widget_id: int, db: Session = Depends(get_db)):
    try:
        result_widget = WidgetUsecases(db).delete(site_id, widget_id)
        return result_widget
    except (SiteNotFoundError, WidgetNotFoundError) as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump()
        )
    except WidgetHasRelatedRecordsError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=response_error.model_dump()
        )