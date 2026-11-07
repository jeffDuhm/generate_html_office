from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class CreateWidgetSchema(BaseModel):
    shortcode: str = Field(min_length=1, max_length=50)
    
class UpdateWidgetSchema(BaseModel):
    shortcode: Optional[str] = Field(default=None, min_length=1, max_length=50)
    is_active: Optional[bool] = None
    
class WidgetSchema(BaseModel):
    id: int
    site_id: int
    shortcode: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)