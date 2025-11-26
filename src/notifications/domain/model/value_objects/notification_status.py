from enum import Enum


class NotificationStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    READ = "READ"

    @classmethod
    def from_string(cls, value: str) -> "NotificationStatus":
        try:
            return cls(value)
        except ValueError as exc:
            raise ValueError(f"Invalid notification status: {value}") from exc
