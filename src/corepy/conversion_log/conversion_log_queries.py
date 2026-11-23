from typing import Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from corepy.conversion_log.conversion_log_dbs import ConversionLogsDB

class ConversionLogQueries:
    
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, user_id: int, site_id: int, filename: str, status: str, error_message: Optional[str]) -> ConversionLogsDB:
        db_conversion_log = ConversionLogsDB(
            user_id=user_id,
            site_id=site_id,
            filename=filename,
            error_message=error_message,
            status=status
        )
        self.db.add(db_conversion_log)
        self.db.commit()
        self.db.refresh(db_conversion_log)
        return db_conversion_log

    def search(self, limit: int, offset: int, status: Optional[str] = None, user_id: Optional[int] = None, site_id: Optional[int] = None) -> Tuple[int, list[ConversionLogsDB]]:
        
        query = select(ConversionLogsDB)

        if status is not None:
            query = query.where(ConversionLogsDB.status == status)
        if user_id is not None:
            query = query.where(ConversionLogsDB.user_id == user_id)
        if site_id is not None:
            query = query.where(ConversionLogsDB.site_id == site_id)

        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.scalar(count_query) or 0
        
        page_query = query.order_by(ConversionLogsDB.id.desc()).limit(limit).offset(offset)
        db_conversion_logs = self.db.scalars(page_query).all()

        return total, db_conversion_logs