from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

def format_url(value: str):
    value = value.strip()
    
    if not value:
        raise ValueError("URL cannot be empty")
    
    if not value.startswith(("http://", "https://")):
        raise ValueError("Url must be valid")
    
    return value

class CreateUrlReplacementSchema(BaseModel):
    source_url: str = Field(min_length=3, max_length=255)
    target_url: str = Field(min_length=3, max_length=255)
    
    @field_validator("source_url", "target_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return format_url(value)
    
class UpdateUrlReplacementSchema(BaseModel):
    source_url: Optional[str] = Field(default=None, min_length=3, max_length=255)
    target_url: Optional[str] = Field(default=None, min_length=3, max_length=255)
    
    @field_validator("source_url", "target_url")
    @classmethod
    def validate_url(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        
        return format_url(value)
    
class UrlReplacementSchema(BaseModel):
    id: int
    site_id: int
    source_url: str
    target_url: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)