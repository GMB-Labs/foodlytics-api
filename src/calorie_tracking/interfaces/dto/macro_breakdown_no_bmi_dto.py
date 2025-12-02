from pydantic import BaseModel


class MacroBreakdownNoBmiDTO(BaseModel):
    calories: float
    protein: float
    carbs: float
    fats: float
