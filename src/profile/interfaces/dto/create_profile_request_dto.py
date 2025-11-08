from pydantic import BaseModel, Field

class CreateProfileDTO(BaseModel):
    user_id: str = Field(..., description="Auth0 user identifier.")
    nutritionist_id: str | None = Field(
        None, description="Assigned nutritionist identifier. Leave empty for nutritionists."
    )
    first_name: str
    last_name: str
    age: int = Field(..., ge=0)
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    gender: str = Field(..., description="Allowed values: male, female, other.")
    goal_type: str = Field(..., description="Allowed values: definition, maintenance, bulking.")
