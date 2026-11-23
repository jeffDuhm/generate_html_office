from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.dependencies import require_admin
from corepy.conversion_log.conversion_log_usecases import ConversionLogUsecases
from corepy.shared.mysql.base import get_db

router = APIRouter(dependencies=[Depends(require_admin)])

@router.get("")
def get_conversion_logs(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None, pattern="^(success|error)$", description="Search by key: \"success\" or \"error\""),
    user_id: Optional[int] = Query(None),
    site_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    result_logs = ConversionLogUsecases(db).get_page(
        page=page,
        per_page=per_page,
        status=status,
        user_id=user_id,
        site_id=site_id
    )
    
    return result_logs