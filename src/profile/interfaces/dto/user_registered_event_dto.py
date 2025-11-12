from pydantic import BaseModel, Field


class UserRegisteredEventDTO(BaseModel):
    user_id: str = Field(..., description="Auth0 user identifier.")
    role: str = Field(..., description="User role, e.g., patient or nutritionist.")
