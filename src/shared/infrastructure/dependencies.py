from functools import lru_cache

from src.iam.domain.services.token_validation_service import TokenValidationService
from src.iam.application.internal.outboundservices.token_validation_service_impl import Auth0TokenValidationServiceImpl
from src.shared.domain.events.event_bus import EventBus
from src.shared.infrastructure.events.in_memory_event_bus import InMemoryEventBus

@lru_cache()
def get_token_validation_service() -> TokenValidationService:
    """
    Provides a cached instance of the Auth0TokenValidationServiceImpl.
    """
    return Auth0TokenValidationServiceImpl()


@lru_cache()
def get_event_bus() -> EventBus:
    """
    Provides a singleton in-memory event bus so bounded contexts can communicate.
    """
    return InMemoryEventBus()
