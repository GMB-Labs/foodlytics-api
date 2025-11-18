from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import DailyIntakeComparisonService
from src.calorie_tracking.application.internal.services.nutritionist_daily_results_service import (
    NutritionistDailyResultsService,
)
from src.calorie_tracking.infrastructure.dependencies import (
    get_calorie_target_service,
    get_daily_comparison_service,
    get_nutritionist_daily_results_service,
)
from src.calorie_tracking.interfaces.dto.calorie_target_dto import CalorieTargetResponseDTO
from src.calorie_tracking.interfaces.dto.daily_intake_summary_dto import DailyIntakeSummaryDTO
from src.calorie_tracking.interfaces.dto.nutritionist_daily_summaries_dto import (
    NutritionistDailySummariesDTO,
    NutritionistDailyRangeSummariesDTO,
)


class CalorieTrackingController:
    def __init__(self):
        self.router = APIRouter(prefix="/calorie-targets", tags=["Calorie Tracking"])
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.get(
            "/{patient_id}/daily-summary",
            response_model=DailyIntakeSummaryDTO,
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
                summary = service.finalize_day(patient_id=patient_id, day=day)
                return {
                    "day": day,
                    "patient_id": patient_id,
                    "target": {
                        "calories": summary.target_calories,
                        "protein": summary.target_protein,
                        "carbs": summary.target_carbs,
                        "fats": summary.target_fats,
                    },
                    "consumed": {
                        "calories": summary.consumed_calories,
                        "protein": summary.consumed_protein,
                        "carbs": summary.consumed_carbs,
                        "fats": summary.consumed_fats,
                    },
                    "difference": {
                        "calories": summary.target_calories - summary.consumed_calories,
                        "protein": summary.target_protein - summary.consumed_protein,
                        "carbs": summary.target_carbs - summary.consumed_carbs,
                        "fats": summary.target_fats - summary.consumed_fats,
                    },
                    "status": summary.status,
                }
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

        @self.router.get("", response_model=List[CalorieTargetResponseDTO])
        def list_targets(
            service: CalorieTargetService = Depends(get_calorie_target_service),
        ):
            targets = service.list_all()
            return [CalorieTargetResponseDTO.from_domain(target) for target in targets]

        @self.router.get("/{patient_id}", response_model=CalorieTargetResponseDTO)
        def get_target(
            patient_id: str,
            service: CalorieTargetService = Depends(get_calorie_target_service),
        ):
            target = service.get_by_patient(patient_id)
            if not target:
                raise HTTPException(
                    status_code=404,
                    detail="Calorie target not found for this patient.",
                )
            return CalorieTargetResponseDTO.from_domain(target)
