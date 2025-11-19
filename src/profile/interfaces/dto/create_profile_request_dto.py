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
    goal_type: str | None = Field(
        None, description="Allowed values: definition, maintenance, bulking. Opcional."
    )
    activity_level: str | None = Field(
        None, description="sedentary, light, active, very_active. Opcional."
    )
    desired_weight_kg: float | None = Field(
        None, gt=0, description="Peso objetivo opcional en kg."
    )
    user_profile_completed: bool = Field(
        False, description="Marca si el usuario completó su perfil. Por defecto False."
    )
