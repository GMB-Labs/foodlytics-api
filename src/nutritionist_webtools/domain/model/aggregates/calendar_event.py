from dataclasses import dataclass
from datetime import date, time
from uuid import uuid4


@dataclass(slots=True)
class CalendarEvent:
    id: str
    nutritionist_id: str
    event_name: str
    event_date: date
    event_time: time

    @classmethod
    def create(
        cls,
        *,
        nutritionist_id: str,
        event_name: str,
        event_date: date,
        event_time: time,
    ) -> "CalendarEvent":
        return cls(
            id=str(uuid4()),
            nutritionist_id=nutritionist_id,
            event_name=event_name,
            event_date=event_date,
            event_time=event_time,
        )
