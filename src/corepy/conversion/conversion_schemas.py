from typing import Optional

from pydantic import BaseModel

class ConversionResultSchema(BaseModel):
    filename: str
    status: str
    html: Optional[str] = None
    error: Optional[str] = None