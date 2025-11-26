from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, String, func

from src.notifications.domain.model.value_objects.notification_status import NotificationStatus
from src.notifications.domain.model.value_objects.notification_type import NotificationType
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base


class NotificationModel(Base):
    __tablename__ = "notifications"

    notification_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(NotificationStatus), nullable=False, default=NotificationStatus.SCHEDULED)
    # Use a different attribute name to avoid clashing with SQLAlchemy's reserved "metadata"
    meta_data = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
