from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

def format_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty")
    return text

class CreateModalMatchSchema(BaseModel):
    text: str = Field(min_length=3, max_length=100)
    
    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return format_text(value)
    
class UpdateModalMatchSchema(BaseModel):
    text: Optional[str] = Field(default=None, min_length=3, max_length=100)
    
    @field_validator("text")
    @classmethod
    def validate_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return format_text(value)
    
class ModalMatchSchema(BaseModel):
    id: int
    site_id: int
    text: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)