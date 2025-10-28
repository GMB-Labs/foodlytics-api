from dataclasses import dataclass
from typing import List, Optional
from src.iam.domain.value_objects.user_role import UserRole


@dataclass
class User:
    id: str
    username: str
    email: Optional[str]
    role: UserRole
    scopes: List[str]
    permissions: List[str]

    @classmethod
    def from_auth0_payload(cls, payload: dict) -> "User":
        sub = payload.get("sub")
        email = payload.get("email")
        scope_raw = payload.get("scope", "")
        permissions = payload.get("permissions", [])

        scopes = scope_raw.split() if isinstance(scope_raw, str) else list(scope_raw)

        if "nutritionist" in scopes or "nutritionist" in permissions:
            role = UserRole.NUTRITIONIST
        else:
            role = UserRole.PATIENT

        username = email if email else sub

        return cls(
            id=sub,
            username=username,
            email=email,
            role=role,
            scopes=scopes,
            permissions=permissions
        )

    # --- Reglas de dominio opcionales ---
    def has_permission(self, perm: str) -> bool:
        """Verifica si el usuario posee un permiso específico."""
        return perm in self.permissions or perm in self.scopes

    def is_patient(self) -> bool:
        return self.role == UserRole.PATIENT

    def is_nutritionist(self) -> bool:
        return self.role == UserRole.NUTRITIONIST
