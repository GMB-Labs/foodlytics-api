from pydantic import BaseModel
from typing import Optional
class UserRequestDTO(BaseModel):
    sub: str
    email: Optional[str] = None
    scope: Optional[str] = None
    permissions: Optional[list[str]] = []