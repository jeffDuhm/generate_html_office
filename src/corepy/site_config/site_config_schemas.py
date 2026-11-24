from pydantic import BaseModel

from corepy.widget_match.widget_match_schemas import WidgetMatchSchema
from corepy.modal_match.modal_match_schemas import ModalMatchSchema
from corepy.url_replacement.url_replacement_schemas import UrlReplacementSchema

class WidgetConfigSchema(BaseModel):
    id: int
    shortcode: str
    matches: list[WidgetMatchSchema]

class SiteConfigSchema(BaseModel):
    site_id: int
    site_name: str
    widgets: list[WidgetConfigSchema]
    modal_matches: list[ModalMatchSchema]
    url_replacements: list[UrlReplacementSchema]