from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ConversionLogSchema(BaseModel):
    id: int
    user_id: int
    site_id: int
    filename: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ConversionLogPageSchema(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    items: list[ConversionLogSchema]