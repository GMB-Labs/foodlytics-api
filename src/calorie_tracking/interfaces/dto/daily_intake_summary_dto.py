from datetime import date
from pydantic import BaseModel


class MacroBreakdownDTO(BaseModel):
    calories: float
    protein: float
    carbs: float
    fats: float
    bmi: float | None = None


class MacroBreakdownNoBmiDTO(BaseModel):
    calories: float
    protein: float
    carbs: float
    fats: float


class DailyIntakeSummaryDTO(BaseModel):
    day: date
    patient_id: str
    target: MacroBreakdownDTO
    consumed: MacroBreakdownDTO
    difference: MacroBreakdownDTO
    status: str
    activity_burned: float = 0
    net_calories: float | None = None


class DailyIntakeSummaryNoBmiDTO(BaseModel):
    day: date
    patient_id: str
    target: MacroBreakdownNoBmiDTO
    consumed: MacroBreakdownNoBmiDTO
    difference: MacroBreakdownNoBmiDTO
    status: str
    activity_burned: float = 0
    net_calories: float | None = None
