from dataclasses import dataclass
from typing import List, Optional
from src.iam.domain.model.value_objects.user_role import UserRole
from src.shared.domain.model.aggregates.auditable_aggregate_root import AuditableAbstractAggregateRoot
from src.shared.domain.model.entities.auditable_model import AuditableModel


@dataclass
class  User(AuditableAbstractAggregateRoot):
    id: str
    username: str
    email: Optional[str]
    role: UserRole
    scopes: List[str]
    permissions: List[str]

    @classmethod
    def from_auth0_payload(cls, payload: dict, role: UserRole) -> "User":
        sub = payload.get("sub")
        email = payload.get("email") or payload.get("https://foodlytics.app/email")
        scope_raw = payload.get("scope", "")
        permissions = payload.get("permissions", [])

        scopes = scope_raw.split() if isinstance(scope_raw, str) else list(scope_raw)

        username = email if email else sub

        return cls(
            id=sub,
            username=username,
            email=email,
            role=role,
            scopes=scopes,
            permissions=permissions
        )

    def has_permission(self, perm: str) -> bool:
        return perm in self.permissions or perm in self.scopes

    def is_patient(self) -> bool:
        return self.role == UserRole.PATIENT

    def is_nutritionist(self) -> bool:
        return self.role == UserRole.NUTRITIONIST
