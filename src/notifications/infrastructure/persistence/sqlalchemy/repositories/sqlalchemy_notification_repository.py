from typing import List, Optional

from sqlalchemy.orm import Session

from src.notifications.domain.model.entities.notification import Notification
from src.notifications.domain.model.value_objects.notification_status import NotificationStatus
from src.notifications.domain.model.value_objects.notification_type import NotificationType
from src.notifications.domain.repositories.notification_repository import NotificationRepository
from src.notifications.infrastructure.persistence.sqlalchemy.models.notification_model import NotificationModel


class SqlAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, notification: Notification) -> Notification:
        model = self.db.get(NotificationModel, notification.notification_id)
        if model is None:
            model = NotificationModel(notification_id=notification.notification_id)
            self.db.add(model)
        self._sync_model(model, notification)
        self.db.commit()
        return notification

    def get(self, notification_id: str) -> Optional[Notification]:
        model = self.db.get(NotificationModel, notification_id)
        if not model:
            return None
        return self._to_domain(model)

    def list_all(self) -> List[Notification]:
        models = self.db.query(NotificationModel).order_by(NotificationModel.scheduled_at.desc()).all()
        return [self._to_domain(model) for model in models]

    def list_by_user(self, user_id: str) -> List[Notification]:
        models = (
            self.db.query(NotificationModel)
            .filter(NotificationModel.user_id == user_id)
            .order_by(NotificationModel.scheduled_at.desc())
            .all()
        )
        return [self._to_domain(model) for model in models]

    def delete(self, notification_id: str) -> None:
        model = self.db.get(NotificationModel, notification_id)
        if model:
            self.db.delete(model)
            self.db.commit()

    def _to_domain(self, model: NotificationModel) -> Notification:
        return Notification(
            notification_id=model.notification_id,
            user_id=model.user_id,
            type=NotificationType(model.type),
            scheduled_at=model.scheduled_at,
            status=NotificationStatus(model.status),
            metadata=model.meta_data or None,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _sync_model(self, model: NotificationModel, entity: Notification) -> None:
        model.user_id = entity.user_id
        model.type = entity.type
        model.scheduled_at = entity.scheduled_at
        model.status = entity.status
        model.meta_data = entity.metadata
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
