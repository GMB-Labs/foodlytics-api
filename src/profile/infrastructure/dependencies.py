from fastapi import Depends
from sqlalchemy.orm import Session

from src.profile.application.internal.commandservices.profile_command_service import ProfileCommandService
from src.profile.application.internal.services.nutritionist_invite_service import NutritionistInviteService
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.infrastructure.persistance.sqlalchemy.repositories.sqlalchemy_profile_repository import (
    SqlAlchemyProfileRepository,
)
from src.profile.domain.repositories.nutritionist_invite_code_repository import (
    NutritionistInviteCodeRepository,
)
from src.profile.infrastructure.persistance.sqlalchemy.repositories.sqlalchemy_nutritionist_invite_code_repository import (
    SqlAlchemyNutritionistInviteCodeRepository,
)
from src.shared.domain.events.event_bus import EventBus
from src.shared.infrastructure.dependencies import get_event_bus
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_profile_repository(db: Session = Depends(get_db)) -> ProfileRepository:
    return SqlAlchemyProfileRepository(db)


def get_nutritionist_invite_code_repository(db: Session = Depends(get_db)) -> NutritionistInviteCodeRepository:
    return SqlAlchemyNutritionistInviteCodeRepository(db)


def get_profile_command_service(
    repository: ProfileRepository = Depends(get_profile_repository),
    event_bus: EventBus = Depends(get_event_bus),
) -> ProfileCommandService:
    return ProfileCommandService(repository, event_bus)


def get_nutritionist_invite_service(
    invite_repo: NutritionistInviteCodeRepository = Depends(get_nutritionist_invite_code_repository),
    profile_repo: ProfileRepository = Depends(get_profile_repository),
) -> NutritionistInviteService:
    return NutritionistInviteService(invite_repo, profile_repo)
