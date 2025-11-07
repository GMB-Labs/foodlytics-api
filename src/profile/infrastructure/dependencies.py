from fastapi import Depends
from sqlalchemy.orm import Session

from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.domain.services.profile_command_service import ProfileCommandService
from src.profile.infrastructure.persistance.sqlalchemy.repositories.sqlalchemy_profile_repository import (
    SqlAlchemyProfileRepository,
)
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_profile_repository(db: Session = Depends(get_db)) -> ProfileRepository:
    return SqlAlchemyProfileRepository(db)


def get_profile_command_service(
    repository: ProfileRepository = Depends(get_profile_repository),
) -> ProfileCommandService:
    return ProfileCommandService(repository)
