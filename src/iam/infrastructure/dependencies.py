from fastapi import Depends
from sqlalchemy.orm import Session
from src.shared.infrastructure.dependencies import get_event_bus
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db
from src.iam.domain.repositories.user_repository import UserRepository
from src.iam.infrastructure.persistence.sqlalchemy.repositories.user_repository_impl import SqlAlchemyUserRepository
from src.iam.application.internal.commandservices.user_service_impl import UserService, UserServiceImpl


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(db)

def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    event_bus = Depends(get_event_bus),
) -> UserService:
    return UserServiceImpl(repo, event_bus)
