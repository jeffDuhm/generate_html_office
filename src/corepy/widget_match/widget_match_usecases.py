from sqlalchemy.orm import Session

from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.widget.widget_queries import WidgetQueries
from corepy.widget_match.widget_match_exceptions import (
    InvalidWidgetMatchUpdateError,
    WidgetMatchConflictError,
    WidgetMatchNotFoundError,
    WidgetNotFoundError,
    WidgetMatchInUseError
)
from corepy.widget_match.widget_match_messages import SuccessWidgetMatchMessages
from corepy.widget_match.widget_match_queries import WidgetMatchQueries
from corepy.widget_match.widget_match_schemas import (
    CreateWidgetMatchSchema,
    UpdateWidgetMatchSchema,
    WidgetMatchSchema,
)

class WidgetMatchUsecases:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_by_site(self, site_id: int, user_id: int) -> ResponseSuccessSchema:
        db_matches = WidgetMatchQueries(self.db).get_all_by_site(site_id, user_id)
        
        matches = []
        
        for db_match in db_matches:
            match = WidgetMatchSchema.model_validate(db_match)
            matches.append(match)
        
        return ResponseSuccessSchema(
            message=SuccessWidgetMatchMessages.WIDGET_MATCH_LIST,
            data=matches
        )
        
    def create(self, widget_id: int, user_id: int, new_match: CreateWidgetMatchSchema) -> ResponseSuccessSchema:
        db_widget = WidgetQueries(self.db).get_by_id(widget_id)
        if not db_widget or not db_widget.is_active:
            raise WidgetNotFoundError()
        
        queries = WidgetMatchQueries(self.db)
        existing = queries.get_by_site_match(
            db_widget.site_id, user_id, new_match.text
        )
        
        if existing is not None:
            if existing.widget_id != widget_id:
                raise WidgetMatchConflictError()
            
            return ResponseSuccessSchema(
                message=SuccessWidgetMatchMessages.WIDGET_MATCH_EXISTS,
                data=WidgetMatchSchema.model_validate(existing)
            )
            
        db_match = queries.create(widget_id,user_id, new_match.text)
        
        match = WidgetMatchSchema.model_validate(db_match)
        
        return ResponseSuccessSchema(
            message=SuccessWidgetMatchMessages.WIDGET_MATCH_CREATED,
            data=match
        )
    
    def update(self, match_id: int, user_id: int, match_update: UpdateWidgetMatchSchema) -> ResponseSuccessSchema:
        
        queries = WidgetMatchQueries(self.db)
        
        db_match = queries.get_by_id(match_id)
        
        if not db_match or db_match.user_id != user_id:
            raise WidgetMatchNotFoundError()
        
        updates = match_update.model_dump(exclude_unset=True)
        
        if not updates:
            raise InvalidWidgetMatchUpdateError()

        for value in updates.values():
            if value is None:
                raise InvalidWidgetMatchUpdateError()

        site_id = db_match.widget.site_id
        
        existing = queries.get_by_site_match(site_id, user_id, updates["text"])
        if existing is not None and existing.id != match_id:
            raise WidgetMatchConflictError()

        db_match = queries.update(db_match, updates)
        
        match = WidgetMatchSchema.model_validate(db_match)

        return ResponseSuccessSchema(
            message=SuccessWidgetMatchMessages.WIDGET_MATCH_UPDATED,
            data=match
        )
        
    def delete(self, match_id: int, user_id: int) -> ResponseSuccessSchema:
        
        queries = WidgetMatchQueries(self.db)
        
        db_match = queries.get_by_id(match_id)
        if not db_match or db_match.user_id != user_id:
            raise WidgetMatchNotFoundError()

        deleted = queries.delete(db_match)
        if not deleted:
            raise WidgetMatchInUseError()

        return ResponseSuccessSchema(message=SuccessWidgetMatchMessages.WIDGET_MATCH_DELETED)