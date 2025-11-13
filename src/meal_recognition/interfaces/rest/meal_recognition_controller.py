from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from src.meal_recognition.application.recognize_meal import MealRecognitionService
from src.meal_recognition.interfaces.dto.meal_recognition_response_dto import MealRecognitionResponseDTO


def get_meal_recognition_service():
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
        async def analyze_meal(
            image: UploadFile = File(...),
            service: MealRecognitionService = Depends(get_meal_recognition_service),
        ):
            image_bytes = await image.read()
            data = service.analyze_meal(image_bytes)

            if "error" in data:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=data
                )

            return data
