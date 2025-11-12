import datetime

from src.iam.domain.model.value_objects.user_role import UserRole
from src.shared.domain.events.domain_event import DomainEvent



class UserRegisteredEvent(DomainEvent):
    def __init__(self, user_id: str, role: UserRole, occurred_on: datetime = None):
        super().__init__(self,occurred_on)
        self.user_id = user_id
        self.role = role

    def __repr__(self):
        return f"UserRegisteredEvent(user_id={self.user_id}, role={self.role})"