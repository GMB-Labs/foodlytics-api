from abc import ABC, abstractmethod
from typing import List, Optional

from src.nutritionist_webtools.domain.model.aggregates.calendar_event import CalendarEvent


class CalendarEventRepository(ABC):
    @abstractmethod
    def list_by_nutritionist(self, nutritionist_id: str) -> List[CalendarEvent]:
        ...

    @abstractmethod
    def find_by_id(self, event_id: str) -> Optional[CalendarEvent]:
        ...

    @abstractmethod
    def save(self, event: CalendarEvent) -> None:
        ...

    @abstractmethod
    def delete(self, event: CalendarEvent) -> None:
        ...
