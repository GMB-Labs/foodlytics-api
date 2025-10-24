import requests
from typing import Dict
from src.shared.infrastructure.settings import settings
from src.iam.domain.services.auth_service import AuthService

class AuthServiceImpl(AuthService):

    def __init__(self):
        self.domain = settings.AUTH0_DOMAIN
        self.client_id = settings.AUTH0_CLIENT_ID
        self.redirect_uri = "http://localhost:8000/auth/callback"

    def exchange_code_for_token(self, code: str, code_verifier:str) -> Dict:
        """
        Exchanges the authorization code for access tokens.
        :param code:
        :param code_verifier:
        :return:
        """
        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": settings.AUTH0_CLIENT_ID,
            "code_verifier": code_verifier,
            "code": code,
            "redirect_uri": settings.AUTH0_REDIRECT_URI
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(token_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
