from fastapi import APIRouter, Depends, HTTPException, status

from src.physical_activity.application.internal.services.physical_activity_service import (
    PhysicalActivityService,
)
from src.physical_activity.infrastructure.dependencies import get_physical_activity_service
from src.physical_activity.interfaces.dto.physical_activity_dto import (
    ActivityAIRequestDTO,
    ActivityCaloriesResponseDTO,
    StepsActivityRequestDTO,
    StepsCaloriesResponseDTO,
)


class PhysicalActivityController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/physical-activity", tags=["Physical Activity"]
        )
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.post(
            "/ai-burn",
            response_model=ActivityCaloriesResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Calcula calorías quemadas usando un servicio externo (IA).",
        )
        def estimate_with_ai(
            payload: ActivityAIRequestDTO,
            service: PhysicalActivityService = Depends(get_physical_activity_service),
        ):
            try:
                return service.estimate_with_ai(
                    user_id=payload.user_id,
                    activity_type=payload.activity_type,
                    duration_minutes=payload.duration_minutes,
                    intensity=payload.intensity,
                )
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc

        @self.router.post(
            "/steps-burn",
            response_model=StepsCaloriesResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Convierte pasos diarios a calorías quemadas.",
        )
        def estimate_from_steps(
            payload: StepsActivityRequestDTO,
            service: PhysicalActivityService = Depends(get_physical_activity_service),
        ):
            try:
                return service.estimate_from_steps(
                    user_id=payload.user_id,
                    steps=payload.steps,
                    step_length_cm=payload.step_length_cm,
                )
            except ValueError as exc:
                status_code = (
                    status.HTTP_400_BAD_REQUEST if "steps must be" in str(exc) else status.HTTP_404_NOT_FOUND
                )
                raise HTTPException(status_code=status_code, detail=str(exc)) from exc
