from datetime import datetime
from typing import Dict, List, Optional

from src.notifications.domain.model.entities.notification import Notification
from src.notifications.domain.model.value_objects.notification_status import NotificationStatus
from src.notifications.domain.model.value_objects.notification_type import NotificationType
from src.notifications.domain.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def create_notification(
        self,
        *,
        notification_id: str,
        user_id: str,
        type: str | NotificationType,
        scheduled_at: datetime,
        status: str | NotificationStatus,
        metadata: Optional[Dict] = None,
    ) -> Notification:
        if self.repository.get(notification_id):
            raise ValueError("Notification already exists.")

        notif_type = NotificationType.from_string(type) if isinstance(type, str) else type
        notif_status = NotificationStatus.from_string(status) if isinstance(status, str) else status

        notification = Notification.create(
            notification_id=notification_id,
            user_id=user_id,
            type=notif_type,
            scheduled_at=scheduled_at,
            status=notif_status,
            metadata=metadata,
        )
        return self.repository.save(notification)

    def list_notifications(self) -> List[Notification]:
        return self.repository.list_all()

    def get_notification(self, notification_id: str) -> Notification:
        notification = self.repository.get(notification_id)
        if not notification:
            raise ValueError("Notification not found.")
        return notification

    def list_by_user(self, user_id: str) -> List[Notification]:
        return self.repository.list_by_user(user_id)

    def delete_notification(self, notification_id: str) -> None:
        if not self.repository.get(notification_id):
            raise ValueError("Notification not found.")
        self.repository.delete(notification_id)
