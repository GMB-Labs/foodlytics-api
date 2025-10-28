from abc import ABC, abstractmethod
from typing import Dict

class AuthService(ABC):
    """
    Abstract service for handling authentication-related operations.
    """
    @abstractmethod
    def get_machine_token(self) -> Dict:
        """
        Obtain a machine-to-machine authentication token for testing
        """
        pass