from datetime import datetime

from pydantic import BaseModel

from src.calorie_tracking.domain.model.entities.calorie_target import CalorieTarget


class CalorieTargetResponseDTO(BaseModel):
    patient_id: str
    calories: float
    protein_grams: float
    carb_grams: float
    fat_grams: float
    bmi: float | None = None
    updated_at: datetime

    @classmethod
    def from_domain(cls, target: CalorieTarget, bmi: float | None = None) -> "CalorieTargetResponseDTO":
        return cls(
            patient_id=target.patient_id,
            calories=target.calories,
            protein_grams=target.protein_grams,
            carb_grams=target.carb_grams,
            fat_grams=target.fat_grams,
            bmi=bmi,
            updated_at=target.updated_at,
        )
