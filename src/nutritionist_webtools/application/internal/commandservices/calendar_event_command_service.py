from datetime import date, time
from typing import List

from src.nutritionist_webtools.domain.model.aggregates.calendar_event import CalendarEvent
from src.nutritionist_webtools.domain.repositories.calendar_event_repository import CalendarEventRepository


class CalendarEventCommandService:
    def __init__(self, event_repository: CalendarEventRepository):
        self.event_repository = event_repository

    def create_event(
        self,
        *,
        nutritionist_id: str,
        event_name: str,
        event_date: date,
        event_time: time,
    ) -> CalendarEvent:
        event = CalendarEvent.create(
            nutritionist_id=nutritionist_id,
            event_name=event_name,
            event_date=event_date,
            event_time=event_time,
        )
        self.event_repository.save(event)
        return event

    def list_events(self, *, nutritionist_id: str) -> List[CalendarEvent]:
        return self.event_repository.list_by_nutritionist(nutritionist_id)

    def delete_event(self, *, event_id: str) -> None:
        event = self.event_repository.find_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        self.event_repository.delete(event)
