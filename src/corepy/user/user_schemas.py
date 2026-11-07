from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

def check_password_rules(value: str) -> str:
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one digit.")
    return value

class UserAuthSchema(BaseModel):
    email: str
    password: str

class CreateUserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    is_admin: bool = False
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return check_password_rules(value)

class UpdateUserSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=72)
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return check_password_rules(value)

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)