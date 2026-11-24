from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.dependencies import get_current_user
from corepy.shared.mysql.base import get_db
from corepy.shared.schemas.response_schemas import ResponseErrorSchema
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.conversion.conversion_exceptions import NoFilesError, InvalidFileTypeError
from corepy.conversion.conversion_usecases import ConversionUsecases

router = APIRouter()

@router.post("/sites/{site_id}/convert")
def convert_files(
    site_id: int,
    files: list[UploadFile] = File(default=[]),
    use_sections: bool = Form(True),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return ConversionUsecases(db).convert(
            user_id=current_user.id,
            site_id=site_id,
            files=files,
            use_sections=use_sections
        )
    except SiteNotFoundError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response_error.model_dump()
        )
    except NoFilesError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_error.model_dump()
        )
    except InvalidFileTypeError as e:
        response_error = ResponseErrorSchema(message=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response_error.model_dump()
        )