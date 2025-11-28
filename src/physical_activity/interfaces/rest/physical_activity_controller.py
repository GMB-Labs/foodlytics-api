from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.physical_activity.application.internal.services.physical_activity_service import (
    PhysicalActivityService,
)
from src.physical_activity.infrastructure.dependencies import get_physical_activity_service
from src.physical_activity.interfaces.dto.physical_activity_dto import (
    ActivityAIRequestDTO,
    ActivityByDayResponseDTO,
    ActivityCaloriesResponseDTO,
    ActivityRangeResponseDTO,
    ActivityUpdateRequestDTO,
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
                    day=payload.day,
                )
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc

        @self.router.put(
            "/ai-burn",
            response_model=ActivityCaloriesResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="(PUT) Calcula calorías quemadas usando un servicio externo (IA).",
        )
        def estimate_with_ai_put(
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
                    day=payload.day,
                    step_length_cm=payload.step_length_cm,
                )
            except ValueError as exc:
                status_code = (
                    status.HTTP_400_BAD_REQUEST if "steps must be" in str(exc) else status.HTTP_404_NOT_FOUND
                )
                raise HTTPException(status_code=status_code, detail=str(exc)) from exc

        @self.router.put(
            "/steps-burn",
            response_model=StepsCaloriesResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="(PUT) Convierte pasos diarios a calorías quemadas.",
        )
        def estimate_from_steps_put(
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

        @self.router.get(
            "/{user_id}",
            response_model=ActivityByDayResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Obtiene calorías quemadas por usuario y fecha.",
        )
        def get_activity_by_day(
            user_id: str,
            date: datetime,
            service: PhysicalActivityService = Depends(get_physical_activity_service),
        ):
            try:
                return service.get_activity_by_day(user_id=user_id, day=date.date())
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc

        # Eliminated delete-by-day endpoint per request.

        @self.router.put(
            "/by-id/{activity_id}",
            response_model=ActivityByDayResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Actualiza datos de actividad física por id.",
        )
        def update_activity_by_id(
            activity_id: str,
            payload: ActivityUpdateRequestDTO,
            service: PhysicalActivityService = Depends(get_physical_activity_service),
        ):
            if (
                payload.activity_burned is None
                and payload.activity_type is None
                and payload.activity_duration_minutes is None
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="At least one field must be provided to update activity.",
                )
            try:
                return service.update_activity_by_id(
                    activity_id=activity_id,
                    activity_burned=payload.activity_burned,
                    activity_type=payload.activity_type,
                    activity_duration_minutes=payload.activity_duration_minutes,
                )
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc

        @self.router.delete(
            "/by-id/{activity_id}",
            response_model=ActivityByDayResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Elimina la actividad física por id.",
        )
        def delete_activity_by_id(
            activity_id: str,
            service: PhysicalActivityService = Depends(get_physical_activity_service),
        ):
            try:
                return service.delete_activity_by_id(activity_id=activity_id)
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc

        @self.router.get(
            "/{user_id}/range",
            response_model=ActivityRangeResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Obtiene calorías quemadas por usuario en un rango de fechas.",
        )
        def get_activity_range(
            user_id: str,
            start_date: date,
            end_date: date,
            service: PhysicalActivityService = Depends(get_physical_activity_service),
        ):
            try:
                return service.get_activity_range(
                    user_id=user_id, start_date=start_date, end_date=end_date
                )
            except ValueError as exc:
                message = str(exc)
                status_code = (
                    status.HTTP_400_BAD_REQUEST
                    if "start_date must be on or before end_date." in message
                    else status.HTTP_404_NOT_FOUND
                )
                raise HTTPException(status_code=status_code, detail=message) from exc
