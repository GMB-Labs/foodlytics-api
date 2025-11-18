from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.infrastructure.dependencies import get_calorie_target_service
from src.calorie_tracking.interfaces.dto.calorie_target_dto import CalorieTargetResponseDTO


class CalorieTrackingController:
    def __init__(self):
        self.router = APIRouter(prefix="/calorie-targets", tags=["Calorie Tracking"])
        self.register_routes()

    def register_routes(self) -> None:
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
