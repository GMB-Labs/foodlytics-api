from fastapi import Depends
from sqlalchemy.orm import Session

from src.calorie_tracking.application.internal.services.calorie_target_service import CalorieTargetService
from src.calorie_tracking.domain.repository.calorie_target_repository import CalorieTargetRepository
from src.calorie_tracking.infrastructure.persistence.sqlalchemy.repository import SqlAlchemyCalorieTargetRepository
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_calorie_target_repository(db: Session = Depends(get_db)) -> CalorieTargetRepository:
    return SqlAlchemyCalorieTargetRepository(db)


def get_calorie_target_service(
    repository: CalorieTargetRepository = Depends(get_calorie_target_repository),
) -> CalorieTargetService:
    return CalorieTargetService(repository)
