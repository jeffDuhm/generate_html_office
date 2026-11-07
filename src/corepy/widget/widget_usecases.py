from sqlalchemy.orm import Session

from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.widget.widget_queries import WidgetQueries
from corepy.widget.widget_schemas import (
    CreateWidgetSchema,
    UpdateWidgetSchema,
    WidgetSchema
)
from corepy.widget.widget_messages import SuccessWidgetMessages
from corepy.widget.widget_exceptions import (
    WidgetNotFoundError,
    WidgetShortcodeAlreadyExistsError,
    WidgetHasRelatedRecordsError,
    WidgetInvalidUpdateError
)
from corepy.site.site_queries import SiteQueries

class WidgetUsecases:
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_all_by_site(self, site_id: int) -> ResponseSuccessSchema:
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        db_widgets = WidgetQueries(self.db).get_all_by_site(site_id)
        
        widgets = []
        for db_widget in db_widgets:
            widgets.append(WidgetSchema.model_validate(db_widget))
        return ResponseSuccessSchema(
            message=SuccessWidgetMessages.WIDGETS_LIST,
            data=widgets
        )
        
    def get_by_id(self, widget_id: int, site_id: int) -> ResponseSuccessSchema:
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        db_widget = WidgetQueries(self.db).get_by_id(widget_id)
        if not db_widget or db_widget.site_id != site_id:
            raise WidgetNotFoundError()

        widget = WidgetSchema.model_validate(db_widget)

        return ResponseSuccessSchema(
            message=SuccessWidgetMessages.WIDGET_GET,
            data=widget
        )
    
    def create(self, site_id: int, new_widget: CreateWidgetSchema) -> ResponseSuccessSchema:
        
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        queries = WidgetQueries(self.db)
        
        if queries.get_by_shortcode(site_id, new_widget.shortcode):
            raise WidgetShortcodeAlreadyExistsError()
        
        db_widget = queries.create(site_id, shortcode=new_widget.shortcode)
        
        widget = WidgetSchema.model_validate(db_widget)
        
        return ResponseSuccessSchema(
            message=SuccessWidgetMessages.WIDGET_CREATED,
            data=widget
        )
        
    def update(self, site_id: int, widget_id: int, widget_update: UpdateWidgetSchema) -> ResponseSuccessSchema:
        
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        queries = WidgetQueries(self.db)
        
        db_widget = queries.get_by_id(widget_id)
        if not db_widget or db_widget.site_id != site_id:
            raise WidgetNotFoundError()
        
        updates = widget_update.model_dump(exclude_unset=True)
        
        if not updates:
            raise WidgetInvalidUpdateError()
        
        for value in updates.values():
            if value is None:
                raise WidgetInvalidUpdateError()
        
        new_shortcode = updates.get("shortcode")
        
        if new_shortcode is not None:
            existing_widget = queries.get_by_shortcode(site_id, new_shortcode)
            if existing_widget is not None and existing_widget.id != widget_id:
                raise WidgetShortcodeAlreadyExistsError()    
        
        db_widget = queries.update(db_widget, updates)
        
        widget = WidgetSchema.model_validate(db_widget)
        
        return ResponseSuccessSchema(
            message=SuccessWidgetMessages.WIDGET_UPDATED,
            data=widget
        )
        
    def delete(self, site_id: int, widget_id: int) -> ResponseSuccessSchema:
        
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        queries = WidgetQueries(self.db)
        
        db_widget = queries.get_by_id(widget_id)
        if not db_widget or db_widget.site_id != site_id:
            raise WidgetNotFoundError()
        
        deleted = queries.delete(db_widget)
        if not deleted:
            raise WidgetHasRelatedRecordsError()
        
        return ResponseSuccessSchema(message=SuccessWidgetMessages.WIDGET_DELETED)