from fastapi import Depends
from sqlalchemy.orm import Session

from src.calorie_tracking.application.internal.queryservices import (
    CalorieTargetQueryService,
    DailyIntakeSummaryQueryService,
    NutritionistDailyResultsQueryService,
    WeightHistoryQueryService,
)
from src.calorie_tracking.application.internal.commandservices.calorie_target_service import CalorieTargetService
from src.calorie_tracking.application.internal.commandservices.daily_intake_comparison_service import DailyIntakeComparisonService
from src.calorie_tracking.application.internal.commandservices.nutritionist_daily_results_service import (
    NutritionistDailyResultsService,
)
from src.calorie_tracking.application.internal.commandservices.weight_history_service import WeightHistoryService
from src.calorie_tracking.domain.repository.calorie_target_repository import CalorieTargetRepository
from src.calorie_tracking.domain.repository.daily_intake_summary_repository import DailyIntakeSummaryRepository
from src.calorie_tracking.domain.repository.weight_history_repository import WeightHistoryRepository
from src.calorie_tracking.infrastructure.persistence.sqlalchemy.repository import (
    SqlAlchemyCalorieTargetRepository,
    SqlAlchemyDailyIntakeSummaryRepository,
    SqlAlchemyWeightHistoryRepository,
)
from src.meal_recognition.domain.repository.meal_repository import MealRepository
from src.meal_recognition.infrastructure.persistence.sqlalchemy.repository.sqlalchemy_meal_repository import SqlAlchemyMealRepository
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.infrastructure.dependencies import get_profile_repository
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_calorie_target_repository(db: Session = Depends(get_db)) -> CalorieTargetRepository:
    return SqlAlchemyCalorieTargetRepository(db)


def get_calorie_target_service(
    repository: CalorieTargetRepository = Depends(get_calorie_target_repository),
) -> CalorieTargetService:
    return CalorieTargetService(repository)

def get_calorie_target_query_service(
    repository: CalorieTargetRepository = Depends(get_calorie_target_repository),
) -> CalorieTargetQueryService:
    return CalorieTargetQueryService(repository)


def get_meal_repository(db: Session = Depends(get_db)) -> MealRepository:
    return SqlAlchemyMealRepository(db)

def get_daily_intake_summary_repository(db: Session = Depends(get_db)) -> DailyIntakeSummaryRepository:
    return SqlAlchemyDailyIntakeSummaryRepository(db)

def get_weight_history_repository(db: Session = Depends(get_db)) -> WeightHistoryRepository:
    return SqlAlchemyWeightHistoryRepository(db)


def get_daily_comparison_service(
    meal_repo: MealRepository = Depends(get_meal_repository),
    target_service: CalorieTargetService = Depends(get_calorie_target_service),
    summary_repo: DailyIntakeSummaryRepository = Depends(get_daily_intake_summary_repository),
    profile_repo: ProfileRepository = Depends(get_profile_repository),
) -> DailyIntakeComparisonService:
    return DailyIntakeComparisonService(meal_repo, target_service, summary_repo, profile_repo)


def get_daily_summary_query_service(
    comparison_service: DailyIntakeComparisonService = Depends(get_daily_comparison_service),
) -> DailyIntakeSummaryQueryService:
    return DailyIntakeSummaryQueryService(comparison_service)


def get_nutritionist_daily_results_service(
    profile_repo: ProfileRepository = Depends(get_profile_repository),
    comparison_service: DailyIntakeComparisonService = Depends(get_daily_comparison_service),
) -> NutritionistDailyResultsService:
    return NutritionistDailyResultsService(profile_repo, comparison_service)


def get_nutritionist_daily_results_query_service(
    profile_repo: ProfileRepository = Depends(get_profile_repository),
    daily_summary_query_service: DailyIntakeSummaryQueryService = Depends(get_daily_summary_query_service),
) -> NutritionistDailyResultsQueryService:
    return NutritionistDailyResultsQueryService(profile_repo, daily_summary_query_service)


def get_weight_history_service(
    weight_history_repo: WeightHistoryRepository = Depends(get_weight_history_repository),
    profile_repo: ProfileRepository = Depends(get_profile_repository),
) -> WeightHistoryService:
    return WeightHistoryService(weight_history_repo, profile_repo)


def get_weight_history_query_service(
    weight_history_repo: WeightHistoryRepository = Depends(get_weight_history_repository),
    profile_repo: ProfileRepository = Depends(get_profile_repository),
) -> WeightHistoryQueryService:
    return WeightHistoryQueryService(weight_history_repo, profile_repo)
