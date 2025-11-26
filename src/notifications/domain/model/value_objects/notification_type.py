from enum import Enum


class NotificationType(str, Enum):
    MEAL_REMINDER = "MEAL_REMINDER"
    BREAKFAST_REMINDER = "BREAKFAST_REMINDER"
    LUNCH_REMINDER = "LUNCH_REMINDER"
    DINNER_REMINDER = "DINNER_REMINDER"
    SNACK_REMINDER = "SNACK_REMINDER"
    WEEKLY_CHECKIN = "WEEKLY_CHECKIN"
    WEIGHT_REMINDER = "WEIGHT_REMINDER"
    WATER_REMINDER = "WATER_REMINDER"
    APPOINTMENT_REMINDER = "APPOINTMENT_REMINDER"

    @classmethod
    def from_string(cls, value: str) -> "NotificationType":
        try:
            return cls(value)
        except ValueError as exc:
            raise ValueError(f"Invalid notification type: {value}") from exc
