from jose import jwt
from jose.exceptions import JWTError
import requests
from src.shared.infrastructure.settings import settings

def verify_jwt(token: str):
    """
    This client verifies the user integrity
    :param token:
    :return:
    """
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    unverified_header = jwt.get_unverified_header(token)

    key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
    if not key:
        raise JWTError("Public key not found.")

    public_key = jwt.construct_key(key)
    payload = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=settings.AUTH0_AUDIENCE,
        issuer=f"https://{settings.AUTH0_DOMAIN}/"
    )
    return payload
