from src.profile.domain.events import ProfileUpdatedEvent
from src.shared.domain.events.event_bus import EventBus

from .profile_updated_event_handler import ProfileUpdatedEventHandler
from .weight_history_event_handler import WeightHistoryEventHandler


def register_calorie_tracking_event_handlers(event_bus: EventBus) -> None:
    """
    Subscribes calorie-tracking event handlers to the shared event bus.
    """
    handler = ProfileUpdatedEventHandler()
    event_bus.subscribe(ProfileUpdatedEvent, handler)
    event_bus.subscribe(ProfileUpdatedEvent, WeightHistoryEventHandler())
