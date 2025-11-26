from fastapi import Depends
from sqlalchemy.orm import Session

from src.notifications.application.notification_service import NotificationService
from src.notifications.domain.repositories.notification_repository import NotificationRepository
from src.notifications.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_notification_repository import (
    SqlAlchemyNotificationRepository,
)
from src.shared.infrastructure.persistence.sqlalchemy.session import get_db


def get_notification_repository(db: Session = Depends(get_db)) -> NotificationRepository:
    return SqlAlchemyNotificationRepository(db)


def get_notification_service(
    repository: NotificationRepository = Depends(get_notification_repository),
) -> NotificationService:
    return NotificationService(repository)
