from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Dict, Iterable, Type, TypeVar

from .domain_event import DomainEvent

E = TypeVar("E", bound=DomainEvent)
EventHandler = Callable[[E], Awaitable[None] | None]


class EventBus(ABC):
    """
    Contract for an application-level event bus.
    """

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """
        Publishes a domain event to all registered subscribers.
        """

    @abstractmethod
    def publish_many(self, events: Iterable[DomainEvent]) -> None:
        """
        Convenience method to publish several events atomically (best-effort).
        """

    @abstractmethod
    def subscribe(self, event_type: Type[E], handler: EventHandler[E]) -> None:
        """
        Registers a handler for a specific event type.
        """
