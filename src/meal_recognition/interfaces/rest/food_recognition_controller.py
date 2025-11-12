from fastapi import APIRouter, Depends, HTTPException, status
from src.meal_recognition.interfaces.dto.meal_recognition_request_dto import MealRecognitionRequestDTO
from src.meal_recognition.interfaces.dto.meal_recognition_response_dto import MealRecognitionResponseDTO
from src.meal_recognition.application.recognize_meal import MealRecognitionService
from src.shared.infrastructure.settings import Settings

def get_meal_recognition_service():
    # Lo ideal es montarlo con settings (pydantic-settings)
    return MealRecognitionService()

class MealRecognitionController:
    def __init__(self):
        self.router = APIRouter(prefix="/recognition", tags=["Meal Recognition"])
        self.register_routes()

    def register_routes(self):
        @self.router.post(
            "/analyze",
            response_model=MealRecognitionResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def analyze_meal(
            body: MealRecognitionRequestDTO,
            service: MealRecognitionService = Depends(get_meal_recognition_service)
        ):
            data = service.analyze_meal(body.image_url)

            if "error" in data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=data
                )

            return data
