from src.iam.domain.events.user_registered_event import UserRegisteredEvent
from src.profile.application.internal.eventhandlers.user_registered_event_handler import (
    UserRegisteredEventHandler,
)
from src.shared.domain.events.event_bus import EventBus


def register_profile_event_handlers(event_bus: EventBus) -> None:
    """
    Registers profile-related event handlers against the shared event bus.
    """
    event_bus.subscribe(UserRegisteredEvent, UserRegisteredEventHandler())
