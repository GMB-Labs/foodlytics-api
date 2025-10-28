from abc import ABC, abstractmethod
from typing import Dict, Any, Callable


class TokenValidationService(ABC):
    @abstractmethod
    def verify_token(self, credentials: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    def require_scope(self, required_scope: str) -> Callable:
        pass


    @abstractmethod
    def get_authenticated_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass
