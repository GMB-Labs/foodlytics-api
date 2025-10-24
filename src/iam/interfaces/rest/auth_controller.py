from fastapi import APIRouter, Query
from src.iam.application.internal.auth_service_impl import AuthServiceImpl

class AuthController:


    def __init__(self):
        self.auth_service= AuthServiceImpl()
        self.router= APIRouter(prefix="/auth", tags=["Auth"])
        self.register_routes()

    def register_routes(self):
        @self.router.get("/login")
        def login():
            domain = self.auth_service.domain
            client_id = self.auth_service.client_id
            url = (
                f"https://{domain}/authorize?"
                f"response_type=code&"
                f"client_id={client_id}&"
                f"redirect_uri={self.auth_service.redirect_uri}&"
                f"scope=openid%20profile%20email&"
                f"code_challenge_method=S256"
            )
            return {"login_url": url}

        @self.router.get("/callback")
        def callback(code:str = Query(...),code_verifier: str = Query(...)):
            """
            Handles the callback from the authentication provider.
            :param code:
            :param code_verifier:
            :return:
            """
            tokens = self.auth_service.exchange_code_for_token(code,code_verifier)
            return tokens