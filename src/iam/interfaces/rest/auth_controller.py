from fastapi import APIRouter, Depends
from src.iam.domain.services.auth_service import AuthService
from src.iam.infrastructure.external.auth0.auth0_machine_service import Auth0MachineService
from src.shared.infrastructure.dependencies import get_token_validation_service
from src.iam.domain.services.token_validation_service import TokenValidationService


class AuthController:
    def __init__(
        self,
        auth_service: AuthService
    ):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/auth", tags=["Auth"])
        self.register_routes()

    def register_routes(self):
        @self.router.get("/token")
        def get_machine_token():
            return self.auth_service.get_machine_token()

        @self.router.get("/me")
        def get_me(
            payload=Depends(get_token_validation_service().verify_token),
            token_service: TokenValidationService = Depends(get_token_validation_service),
        ):
            return token_service.get_authenticated_user(payload)

        @self.router.get("/patient-area")
        def patient_area(payload=Depends(get_token_validation_service().require_scope("patient"))):
            return {"message": "Área del paciente"}

        @self.router.get("/nutritionist-area")
        def nutritionist_area(payload=Depends(get_token_validation_service().require_scope("nutritionist"))):
            return {"message": "Área del nutricionista"}

        @self.router.get("/records")
        def get_records(
                payload=Depends(get_token_validation_service().require_scope("read:diet")),
                _: dict = Depends(get_token_validation_service().require_scope("patient")),
        ):
            return {"message": "El nutricionista puede leer dietas"}
