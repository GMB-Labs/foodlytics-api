from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
from typing import Dict, Any

from src.shared.infrastructure.settings import settings
from src.iam.domain.services.token_validation_service import TokenValidationService


class Auth0TokenValidationServiceImpl(TokenValidationService):
    def __init__(self):
        self.domain = settings.AUTH0_DOMAIN
        self.audience = settings.AUTH0_AUDIENCE
        self.algorithm = settings.AUTH0_ALGORITHMS
        self.security = HTTPBearer()

    def _get_jwks(self) -> Dict[str, Any]:
        jwks_url = f"https://{self.domain}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching JWKS")
        return response.json()

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Dict[str, Any]:
        token = credentials.credentials
        jwks = self._get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = next((key for key in jwks["keys"] if key["kid"] == unverified_header["kid"]), None)
        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid token header")

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=f"https://{self.domain}/"
            )
            return payload
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    #TODO: add require_role
    def require_scope(self, required_scope: str):
        def dependency(payload: Dict[str, Any] = Depends(self.verify_token)):
            scopes = payload.get("scope", "").split()
            if required_scope not in scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required scope: {required_scope}"
                )
            return payload
        return dependency



    def get_authenticated_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "auth0_id": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("roles", []),
            "scopes": payload.get("scope", "").split()
        }
