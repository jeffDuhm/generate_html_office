from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

def format_site_name(value: str) -> str:
    format_value = value.strip()
    if not format_value:
        raise ValueError("Site name cannot be empty")
    return format_value
    
class CreateSiteSchema(BaseModel):
    name: str = Field(min_length=1, max_length=120)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return format_site_name(value)

class UpdateSiteSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    is_active: Optional[bool] = None
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return format_site_name(value)
    
class SiteSchema(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)