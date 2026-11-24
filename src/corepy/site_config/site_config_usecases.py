from sqlalchemy.orm import Session
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.site.site_queries import SiteQueries
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.widget.widget_queries import WidgetQueries
from corepy.widget_match.widget_match_queries import WidgetMatchQueries
from corepy.modal_match.modal_match_queries import ModalMatchQueries
from corepy.url_replacement.url_replacement_queries import UrlReplacementQueries
from corepy.widget_match.widget_match_schemas import WidgetMatchSchema
from corepy.modal_match.modal_match_schemas import ModalMatchSchema
from corepy.url_replacement.url_replacement_schemas import UrlReplacementSchema
from corepy.site_config.site_config_schemas import SiteConfigSchema, WidgetConfigSchema
from corepy.site_config.site_config_messages import SuccessSiteConfigMessages

def get_source_url_length(url_replacement):
    return len(url_replacement.source_url)

class SiteConfigUsecases:

    def __init__(self, db: Session):
        self.db = db

    def get_config(self, user_id: int, site_id: int) -> ResponseSuccessSchema:
        
        site = SiteQueries(self.db).get_by_id(site_id)
        if not site or not site.is_active:
            raise SiteNotFoundError()

        widget_queries = WidgetQueries(self.db)
        widget_match_queries = WidgetMatchQueries(self.db)

        db_widgets = widget_queries.get_active_by_site(site_id)
        widgets = []
        for db_widget in db_widgets:
            db_matches = widget_match_queries.get_all_by_widget(
                user_id=user_id,
                widget_id=db_widget.id,
            )
            matches = []
            for db_match in db_matches:
                matches.append(WidgetMatchSchema.model_validate(db_match))

            widget_config = WidgetConfigSchema(
                id=db_widget.id,
                shortcode=db_widget.shortcode,
                matches=matches,
            )
            widgets.append(widget_config)

        db_modal_matches = ModalMatchQueries(self.db).get_all_by_site(
            user_id=user_id,
            site_id=site_id,
        )
        modal_matches = []
        for db_modal_match in db_modal_matches:
            modal_matches.append(ModalMatchSchema.model_validate(db_modal_match))

        db_url_replacements = UrlReplacementQueries(self.db).get_all_by_site(
            user_id=user_id,
            site_id=site_id,
        )
        url_replacements = []
        for db_url_replacement in db_url_replacements:
            url_replacements.append(UrlReplacementSchema.model_validate(db_url_replacement))

        config = SiteConfigSchema(
            site_id=site.id,
            site_name=site.name,
            widgets=widgets,
            modal_matches=modal_matches,
            url_replacements=url_replacements,
        )
        return ResponseSuccessSchema(
            message=SuccessSiteConfigMessages.SITE_CONFIG_SUCCESS,
            data=config.model_dump(),
        )

    def get_rules(self, user_id: int, site_id: int, use_sections: bool = True) -> dict:

        widget_queries = WidgetQueries(self.db)
        widget_match_queries = WidgetMatchQueries(self.db)

        db_widgets = widget_queries.get_active_by_site(site_id)
        
        widgets = []
        
        for db_widget in db_widgets:
            db_matches = widget_match_queries.get_all_by_widget(
                user_id=user_id,
                widget_id=db_widget.id,
            )
            matches = []
            for db_match in db_matches:
                matches.append(db_match.text)
            widgets.append({"shortcode": db_widget.shortcode, "matches": matches})

        db_modal_matches = ModalMatchQueries(self.db).get_all_by_site(
            user_id=user_id,
            site_id=site_id,
        )
        modal_matches = []
        
        for db_modal_match in db_modal_matches:
            modal_matches.append(db_modal_match.text)

        db_url_replacements = UrlReplacementQueries(self.db).get_all_by_site(
            user_id=user_id,
            site_id=site_id,
        )
        
        db_url_replacements.sort(key=get_source_url_length, reverse=True)
        
        url_replacements = []
        
        for db_url_replacement in db_url_replacements:
            url_replacements.append(
                {
                    "source_url": db_url_replacement.source_url,
                    "target_url": db_url_replacement.target_url,
                }
            )

        return {
            "use_sections": use_sections,
            "widgets": widgets,
            "modal_matches": modal_matches,
            "url_replacements": url_replacements,
        }