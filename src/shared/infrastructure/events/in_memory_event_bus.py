from __future__ import annotations

import asyncio
import inspect
import logging
from collections import defaultdict
from threading import Lock
from typing import Dict, Iterable, List, Type

from src.shared.domain.events.domain_event import DomainEvent
from src.shared.domain.events.event_bus import EventBus, EventHandler

logger = logging.getLogger(__name__)


class InMemoryEventBus(EventBus):
    """
    Simple in-memory event bus that fans out events to subscribed handlers.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[Type[DomainEvent], List[EventHandler]] = defaultdict(list)
        self._lock = Lock()

    def publish(self, event: DomainEvent) -> None:
        handlers = self._collect_handlers(type(event))
        logger.debug(
            "Publishing event %s to %d handler(s)",
            type(event).__name__,
            len(handlers),
        )
        if not handlers:
            return

        for handler in handlers:
            try:
                result = handler(event)
                if inspect.isawaitable(result):
                    self._schedule_async(result)
            except Exception:  # pragma: no cover - log but keep bus alive
                logger.exception("Error while handling event %s with handler %s", event, handler)

    def publish_many(self, events: Iterable[DomainEvent]) -> None:
        for event in events:
            self.publish(event)

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        with self._lock:
            if handler not in self._subscribers[event_type]:
                self._subscribers[event_type].append(handler)
                logger.debug(
                    "Subscribed handler %s to event %s",
                    getattr(handler, "__class__", type(handler)).__name__,
                    event_type.__name__,
                )

    def _collect_handlers(self, event_type: Type[DomainEvent]) -> List[EventHandler]:
        with self._lock:
            matched: List[EventHandler] = []
            for registered_type, handlers in self._subscribers.items():
                if issubclass(event_type, registered_type):
                    matched.extend(handlers)
            return list(matched)

    def _schedule_async(self, awaitable) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(awaitable)
        else:
            asyncio.run(awaitable)
