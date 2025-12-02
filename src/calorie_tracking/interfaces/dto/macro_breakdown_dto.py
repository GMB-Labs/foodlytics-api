from pydantic import BaseModel


class MacroBreakdownDTO(BaseModel):
    calories: float
    protein: float
    carbs: float
    fats: float
    bmi: float | None = None
