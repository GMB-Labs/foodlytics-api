import datetime
from datetime import timedelta, timezone

from src.profile.domain.model.value_objects.gender import Gender
from src.profile.domain.model.value_objects.goal_type import GoalType
from src.profile.domain.model.value_objects.activity_level import ActivityLevel
from src.shared.domain.events.domain_event import DomainEvent


class ProfileUpdatedEvent(DomainEvent):
    def __init__(
        self,
        *,
        user_id: str,
        age: int,
        height_cm: float,
        weight_kg: float,
        gender: Gender,
        goal_type: GoalType,
        activity_level: ActivityLevel | None = None,
        desired_weight_kg: float | None = None,
        occurred_on: datetime.datetime | None = None,
    ):
        utc_minus_5 = timezone(timedelta(hours=-5))
        super().__init__(occurred_on=occurred_on or datetime.datetime.now(utc_minus_5))
        self.user_id = user_id
        self.age = age
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.gender = gender
        self.goal_type = goal_type
        self.activity_level = activity_level
        self.desired_weight_kg = desired_weight_kg

    def __repr__(self) -> str:
        return (
            "ProfileUpdatedEvent(user_id="
            f"{self.user_id}, gender={self.gender}, height_cm={self.height_cm}, weight_kg={self.weight_kg})"
        )
