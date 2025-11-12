from dataclasses import field,dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class DomainEvent:
    """
    Base class for domain events that captures identity and occurrence metadata.
    """

    event_id: UUID = field(default_factory=uuid4)
    occurred_on: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_primitives(self) -> dict:
        """
        Helper for logging/serialization. Subclasses can extend this if needed.
        """
        return {
            "event_id": str(self.event_id),
            "occurred_on": self.occurred_on.isoformat(),
        }
