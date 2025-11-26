from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from src.notifications.domain.model.value_objects.notification_status import NotificationStatus
from src.notifications.domain.model.value_objects.notification_type import NotificationType


class NotificationRequestDTO(BaseModel):
    user_id: str = Field(alias="userId")
    notification_id: str = Field(alias="notificationId")
    type: NotificationType
    scheduled_at: datetime = Field(alias="scheduledAt")
    status: NotificationStatus = NotificationStatus.SCHEDULED
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class NotificationResponseDTO(BaseModel):
    user_id: str = Field(alias="userId")
    notification_id: str = Field(alias="notificationId")
    type: NotificationType
    scheduled_at: datetime = Field(alias="scheduledAt")
    status: NotificationStatus
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

    @classmethod
    def from_domain(cls, notification) -> "NotificationResponseDTO":
        return cls(
            userId=notification.user_id,
            notificationId=notification.notification_id,
            type=notification.type,
            scheduledAt=notification.scheduled_at,
            status=notification.status,
            metadata=notification.metadata,
            createdAt=notification.created_at,
            updatedAt=notification.updated_at,
        )
