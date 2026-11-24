from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.site_config.site_config_usecases import SiteConfigUsecases

router = APIRouter()

@router.get("/sites/{site_id}/config")
def get_site_config(
    site_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        result_site_config = SiteConfigUsecases(db).get_config(
            user_id=current_user.id,
            site_id=site_id,
        )
        return result_site_config
        
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump(),
        )