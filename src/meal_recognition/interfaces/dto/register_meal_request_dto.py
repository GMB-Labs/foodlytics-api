from pydantic import BaseModel
from src.meal_recognition.domain.model.valueobjects.meal_type import MealType

class RegisterMealRequestDTO(BaseModel):
    name: str
    approximate_weight_in_grams: float
    meal_t: MealType
    kcal: float
    protein: float
    carbs: float
    fats: float
