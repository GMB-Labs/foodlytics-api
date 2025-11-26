from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from src.notifications.domain.model.value_objects.notification_status import NotificationStatus
from src.notifications.domain.model.value_objects.notification_type import NotificationType


@dataclass
class Notification:
    notification_id: str
    user_id: str
    type: NotificationType
    scheduled_at: datetime
    status: NotificationStatus
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        *,
        user_id: str,
        type: NotificationType,
        scheduled_at: datetime,
        status: NotificationStatus,
        metadata: Optional[Dict[str, Any]] = None,
        notification_id: Optional[str] = None,
    ) -> "Notification":
        now = datetime.now(timezone.utc)
        generated_id = notification_id or str(uuid4())
        return Notification(
            notification_id=generated_id,
            user_id=user_id,
            type=type,
            scheduled_at=scheduled_at,
            status=status,
            metadata=metadata,
            created_at=now,
            updated_at=now,
        )

    def mark_status(self, status: NotificationStatus) -> None:
        self.status = status
        self.updated_at = datetime.now(timezone.utc)
