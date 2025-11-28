from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import DailyIntakeComparisonService
from src.calorie_tracking.application.internal.services.nutritionist_daily_results_service import (
    NutritionistDailyResultsService,
)
from src.calorie_tracking.infrastructure.dependencies import (
    get_calorie_target_service,
    get_daily_comparison_service,
    get_nutritionist_daily_results_service,
    get_weight_history_service,
)
from src.calorie_tracking.interfaces.dto.calorie_target_dto import CalorieTargetResponseDTO
from src.calorie_tracking.interfaces.dto.daily_intake_summary_dto import (
    DailyIntakeSummaryDTO,
    DailyIntakeSummaryNoBmiDTO,
)
from src.calorie_tracking.interfaces.dto.nutritionist_daily_summaries_dto import (
    NutritionistDailySummariesDTO,
    NutritionistDailyRangeSummariesDTO,
)
from src.calorie_tracking.interfaces.dto.weight_history_dto import (
    WeightHistoryEntryResponseDTO,
    WeightHistoryUpsertRequestDTO,
    WeightHistoryResponseDTO,
)
from src.calorie_tracking.application.internal.services.weight_history_service import WeightHistoryService
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.infrastructure.dependencies import get_profile_repository


class CalorieTrackingController:
    def __init__(self):
        self.router = APIRouter(prefix="/calorie-targets", tags=["Calorie Tracking"])
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.get(
            "/{patient_id}/daily-summary",
            response_model=DailyIntakeSummaryNoBmiDTO,
            summary="Compare daily intake vs. target",
        )
        def get_daily_summary(
            patient_id: str,
            day: date,
            service: DailyIntakeComparisonService = Depends(get_daily_comparison_service),
        ):
            try:
                summary = service.get_daily_summary(patient_id=patient_id, day=day)
                return summary
            except ValueError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

        @self.router.post(
            "/{patient_id}/daily-summary/finalize",
            response_model=DailyIntakeSummaryDTO,
            summary="Cierra el día guardando el consumo vs target",
        )
        def finalize_daily_summary(
            patient_id: str,
            day: date,
            service: DailyIntakeComparisonService = Depends(get_daily_comparison_service),
        ):
            try:
                view = service.get_daily_summary(patient_id=patient_id, day=day)
                service.finalize_day(patient_id=patient_id, day=day)
                return view
            except ValueError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

        @self.router.get(
            "/nutritionists/{nutritionist_id}/daily-summaries",
            response_model=NutritionistDailySummariesDTO,
            summary="Daily results for all patients assigned to a nutritionist",
        )
        def get_daily_summaries_by_nutritionist(
            nutritionist_id: str,
            day: date,
            service: NutritionistDailyResultsService = Depends(get_nutritionist_daily_results_service),
        ):
            try:
                summaries, skipped = service.get_patient_summaries_for_day(
                    nutritionist_id=nutritionist_id, day=day
                )
                return {
                    "nutritionist_id": nutritionist_id,
                    "day": day,
                    "summaries": summaries,
                    "skipped_patients": skipped,
                }
            except ValueError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc

        @self.router.get(
            "/nutritionists/{nutritionist_id}/daily-summaries/range",
            response_model=NutritionistDailyRangeSummariesDTO,
            summary="Daily results for assigned patients across a date range",
        )
        def get_daily_summaries_range(
            nutritionist_id: str,
            start_date: date,
            end_date: date,
            service: NutritionistDailyResultsService = Depends(get_nutritionist_daily_results_service),
        ):
            try:
                days = service.get_patient_summaries_for_range(
                    nutritionist_id=nutritionist_id, start_date=start_date, end_date=end_date
                )
                return {
                    "nutritionist_id": nutritionist_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "days": days,
                }
            except ValueError as exc:
                message = str(exc)
                status_code = 400 if "start_date" in message else 404
                raise HTTPException(status_code=status_code, detail=message) from exc

        @self.router.get(
            "/{patient_id}/weight-history",
            response_model=WeightHistoryResponseDTO,
            summary="Weight changes per day within a date range",
        )
        def get_weight_history(
            patient_id: str,
            start_date: date,
            end_date: date,
            service: WeightHistoryService = Depends(get_weight_history_service),
        ):
            try:
                return service.get_history(
                    user_id=patient_id, start_date=start_date, end_date=end_date
                )
            except ValueError as exc:
                message = str(exc)
                status_code = (
                    status.HTTP_400_BAD_REQUEST
                    if "start_date must be on or before end_date." in message
                    else status.HTTP_404_NOT_FOUND
                )
                raise HTTPException(status_code=status_code, detail=message) from exc

        @self.router.put(
            "/{patient_id}/weight-history",
            response_model=WeightHistoryEntryResponseDTO,
            summary="Registra/actualiza el peso de un día específico",
            status_code=status.HTTP_200_OK,
        )
        def upsert_weight_history(
            patient_id: str,
            payload: WeightHistoryUpsertRequestDTO,
            service: WeightHistoryService = Depends(get_weight_history_service),
        ):
            try:
                return service.record_weight(
                    user_id=patient_id, day=payload.day, weight_kg=payload.weight_kg
                )
            except ValueError as exc:
                message = str(exc)
                status_code = (
                    status.HTTP_400_BAD_REQUEST
                    if "must be" in message or "before end_date" in message
                    else status.HTTP_404_NOT_FOUND
                )
                raise HTTPException(status_code=status_code, detail=message) from exc

        @self.router.get("", response_model=List[CalorieTargetResponseDTO])
        def list_targets(
            service: CalorieTargetService = Depends(get_calorie_target_service),
            profile_repo: ProfileRepository = Depends(get_profile_repository),
        ):
            targets = service.list_all()
            return [
                CalorieTargetResponseDTO.from_domain(
                    target,
                    bmi=self._calculate_bmi(profile_repo, target.patient_id),
                )
                for target in targets
            ]

        @self.router.get("/{patient_id}", response_model=CalorieTargetResponseDTO)
        def get_target(
            patient_id: str,
            service: CalorieTargetService = Depends(get_calorie_target_service),
            profile_repo: ProfileRepository = Depends(get_profile_repository),
        ):
            target = service.get_by_patient(patient_id)
            if not target:
                raise HTTPException(
                    status_code=404,
                    detail="Calorie target not found for this patient.",
                )
            bmi = self._calculate_bmi(profile_repo, patient_id)
            return CalorieTargetResponseDTO.from_domain(target, bmi=bmi)

    @staticmethod
    def _calculate_bmi(profile_repo: ProfileRepository, patient_id: str) -> float | None:
        profile = profile_repo.find_by_user_id(patient_id)
        if not profile or not profile.weight_kg or not profile.height_cm:
            return None
        if profile.height_cm <= 0 or profile.weight_kg <= 0:
            return None
        height_m = profile.height_cm / 100
        return round(profile.weight_kg / (height_m ** 2), 2)
