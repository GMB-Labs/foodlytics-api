from pydantic import BaseModel

class MealRecognitionRequestDTO(BaseModel):
    image_url: str
