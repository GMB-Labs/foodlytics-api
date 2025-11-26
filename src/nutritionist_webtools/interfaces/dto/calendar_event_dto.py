from datetime import date, time
from pydantic import BaseModel, Field

from src.nutritionist_webtools.domain.model.aggregates.calendar_event import CalendarEvent


class CalendarEventRequestDTO(BaseModel):
    event_name: str = Field(..., example="Consulta con paciente")
    event_date: date = Field(..., description="YYYY-MM-DD")
    event_time: time = Field(..., description="HH:MM or HH:MM:SS")


class CalendarEventResponseDTO(BaseModel):
    id: str
    nutritionist_id: str
    event_name: str
    event_date: date
    event_time: time

    @classmethod
    def from_domain(cls, event: CalendarEvent) -> "CalendarEventResponseDTO":
        return cls(
            id=event.id,
            nutritionist_id=event.nutritionist_id,
            event_name=event.event_name,
            event_date=event.event_date,
            event_time=event.event_time,
        )
