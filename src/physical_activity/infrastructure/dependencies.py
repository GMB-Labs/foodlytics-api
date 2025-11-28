from fastapi import Depends

from src.calorie_tracking.application.internal.services.daily_intake_comparison_service import (
    DailyIntakeComparisonService,
)
from src.calorie_tracking.infrastructure.dependencies import get_daily_comparison_service
from src.physical_activity.application.internal.services.physical_activity_service import (
    PhysicalActivityService,
)
from src.physical_activity.domain.repositories.physical_activity_repository import PhysicalActivityRepository
from src.physical_activity.infrastructure.persistence.sqlalchemy.repository.sqlalchemy_physical_activity_repository import (
    SqlAlchemyPhysicalActivityRepository,
)
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.infrastructure.dependencies import get_profile_repository
from src.shared.infrastructure.external.physical_activity_ai_client import (
    PhysicalActivityAIClient,
    StubPhysicalActivityAIClient,
)
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_physical_activity_ai_client() -> PhysicalActivityAIClient:
    return StubPhysicalActivityAIClient()

def get_physical_activity_repository(db=Depends(get_db)) -> PhysicalActivityRepository:
    return SqlAlchemyPhysicalActivityRepository(db)


def get_physical_activity_service(
    ai_client: PhysicalActivityAIClient = Depends(get_physical_activity_ai_client),
    profile_repo: ProfileRepository = Depends(get_profile_repository),
    comparison_service: DailyIntakeComparisonService = Depends(get_daily_comparison_service),
    activity_repo: PhysicalActivityRepository = Depends(get_physical_activity_repository),
) -> PhysicalActivityService:
    return PhysicalActivityService(ai_client, profile_repo, comparison_service, activity_repo)
