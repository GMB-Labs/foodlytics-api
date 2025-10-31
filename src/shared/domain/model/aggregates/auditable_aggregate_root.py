from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

@dataclass
class AuditableAbstractAggregateRoot:
    def __init__(self, aggregate_id: Optional[int] = None):
        self.aggregate_id = aggregate_id
        self.created_at: datetime = datetime.now(timezone.utc)
        self.updated_at: datetime = datetime.now(timezone.utc)