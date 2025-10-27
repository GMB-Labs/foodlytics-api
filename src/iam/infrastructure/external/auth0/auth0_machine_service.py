import requests
from typing import Dict
from src.shared.infrastructure.settings import settings
from src.iam.domain.services.auth_service import AuthService

class Auth0MachineService(AuthService):
    """
    Service for obtaining machine-to-machine authentication tokens from Auth0.
    """
    def __init__(self):
        self.domain = settings.AUTH0_DOMAIN
        self.client_id = settings.AUTH0_CLIENT_ID
        self.client_secret = settings.AUTH0_CLIENT_SECRET
        self.audience = settings.AUTH0_AUDIENCE

    def get_machine_token(self) -> Dict:
        """
        Obtain a machine-to-machine authentication token from Auth0.
        :return:
        """
        url = f"https://{self.domain}/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_userinfo(self,access_token: str):
        response = requests.get(
            f"https://{self.domain}/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
