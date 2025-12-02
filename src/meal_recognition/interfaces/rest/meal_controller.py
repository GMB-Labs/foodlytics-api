from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query

from src.meal_recognition.application.internal.commandservices.meal_command_service import MealCommandService
from src.meal_recognition.application.internal.queryservices.meal_query_service import MealQueryService
from src.meal_recognition.application.recognize_meal import MealRecognitionService
from src.meal_recognition.interfaces.dto.meal_recognition_response_dto import MealRecognitionResponseDTO
from src.meal_recognition.interfaces.dto.meal_response_dto import MealResponseDTO
from src.meal_recognition.interfaces.dto.register_meal_request_dto import RegisterMealRequestDTO
from src.meal_recognition.infrastructure.persistence.sqlalchemy.repository.sqlalchemy_meal_repository import SqlAlchemyMealRepository
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db
from src.calorie_tracking.application.internal.commandservices.daily_intake_comparison_service import DailyIntakeComparisonService
from src.calorie_tracking.infrastructure.dependencies import get_daily_comparison_service


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
            repo = Depends(get_meal_repository),
            comparison_service: DailyIntakeComparisonService = Depends(get_daily_comparison_service),
        ):
            service = MealCommandService(repo)
            meal = service.save_recognized_meal(dto, comparison_service)
            return {
                "id": meal.id,
                "uploaded_at": meal.uploaded_at
            }

        @self.router.get(
            "",
            response_model=List[MealResponseDTO],
            status_code=status.HTTP_200_OK
        )
        def get_meals_by_day(
            day: date = Query(..., description="Fecha en formato YYYY-MM-DD"),
            user_id: str = Query(..., description="ID del usuario"),
            repo = Depends(get_meal_repository)
        ):
            service = MealQueryService(repo)
            meals = service.get_by_day(day, user_id)
            return [
                MealResponseDTO(
                    id=meal.id,
                    name=meal.name,
                    patient_id=meal.patient_id,
                    meal_t=meal.mealType,
                    kcal=meal.kcal,
                    protein=meal.protein,
                    carbs=meal.carbs,
                    fats=meal.fats,
                    uploaded_at=meal.uploaded_at
                )
                for meal in meals
            ]
