from functools import lru_cache
from src.shared.domain.services.token_validation_service import TokenValidationService
from src.shared.infrastructure.external.auth0.token_validation_service_impl import Auth0TokenValidationServiceImpl

@lru_cache()
def get_token_validation_service() -> TokenValidationService:
    """
    Provides a cached instance of the Auth0TokenValidationServiceImpl.
    """
    return Auth0TokenValidationServiceImpl()