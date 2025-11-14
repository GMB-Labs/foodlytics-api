from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from src.meal_recognition.application.internal.commandservices.meal_command_service import MealCommandService
from src.meal_recognition.application.recognize_meal import MealRecognitionService
from src.meal_recognition.interfaces.dto.meal_recognition_response_dto import MealRecognitionResponseDTO
from src.meal_recognition.interfaces.dto.register_meal_request_dto import RegisterMealRequestDTO
from src.meal_recognition.infrastructure.persistence.sqlalchemy.repository.sqlalchemy_meal_repository import SqlAlchemyMealRepository
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_meal_repository(db = Depends(get_db)):
    return SqlAlchemyMealRepository(db)


class MealRecognitionController:
    def __init__(self):
        self.router = APIRouter(prefix="/meals", tags=["Meal Recognition"])
        self.service = MealRecognitionService()
        self.register_routes()

    def register_routes(self):

        @self.router.post(
            "/analyze",
            response_model=MealRecognitionResponseDTO,
            status_code=status.HTTP_200_OK
        )
        async def analyze_meal(image: UploadFile = File(...)):
            try:
                if image.content_type not in ["image/jpeg", "image/png", "image/webp"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El archivo debe ser una imagen JPG, PNG o WEBP"
                    )

                image_bytes = await image.read()
                result = self.service.analyze_meal(image_bytes)

                if "error" in result:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=result["error"]
                    )

                return MealRecognitionResponseDTO(**result)

            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e)
                )


        @self.router.post("/register-meal", status_code=status.HTTP_201_CREATED)
        def register_meal(
            dto: RegisterMealRequestDTO,
            repo = Depends(get_meal_repository)
        ):
            service = MealCommandService(repo)
            meal = service.save_recognized_meal(dto)
            return {
                "id": meal.id,
                "uploaded_at": meal.uploaded_at
            }
