from abc import ABC, abstractmethod
from typing import Dict

class AuthService(ABC):
    """
    Abstract service for handling authentication-related operations.
    """
    @abstractmethod
    def exchange_code_for_token(self, code: str, code_verifier:str)-> Dict:
        """
        Exchanges the authorization code for access tokens.
        :param code:
        :param code_verifier:
        :return:
        """
        pass