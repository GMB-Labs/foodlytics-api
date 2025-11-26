from abc import ABC, abstractmethod
from typing import List, Optional

from src.notifications.domain.model.entities.notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        raise NotImplementedError

    @abstractmethod
    def get(self, notification_id: str) -> Optional[Notification]:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Notification]:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: str) -> List[Notification]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, notification_id: str) -> None:
        raise NotImplementedError
