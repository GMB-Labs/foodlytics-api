from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditableModel:
    created_at: datetime | None = None
    updated_at: datetime | None = None