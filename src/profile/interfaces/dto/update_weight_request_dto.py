from pydantic import BaseModel, Field


class UpdateWeightDTO(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Nuevo peso en kilogramos.")
