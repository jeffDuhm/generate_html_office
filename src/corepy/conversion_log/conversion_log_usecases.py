import math

from sqlalchemy.orm import Session
from typing import Optional

from corepy.conversion_log.conversion_log_messages import SuccessConversionLogMessages
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.conversion_log.conversion_log_queries import ConversionLogQueries
from corepy.conversion_log.conversion_log_schema import ConversionLogPageSchema, ConversionLogSchema

class ConversionLogUsecases:

    def __init__(self, db: Session):
        self.db = db

    def get_page(
        self,
        page: int,
        per_page: int,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        site_id: Optional[int] = None,
    ) -> ResponseSuccessSchema:
        
        offset = (page - 1) * per_page

        total, db_conversion_logs = ConversionLogQueries(self.db).search(
            limit=per_page,
            offset=offset,
            status=status,
            user_id=user_id,
            site_id=site_id,
        )

        items = []
        for db_conversion_log in db_conversion_logs:
            item = ConversionLogSchema.model_validate(db_conversion_log)
            items.append(item)

        total_pages = math.ceil(total / per_page)   

        page_data = ConversionLogPageSchema(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
            items=items,
        )

        return ResponseSuccessSchema(
            message=SuccessConversionLogMessages.CONVERSION_LOGS_LIST,
            data=page_data,
        )