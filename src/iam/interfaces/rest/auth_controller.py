from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from dataclasses import asdict

from src.iam.application.internal.commandservices.user_service_impl import UserService
from src.iam.infrastructure.dependencies import get_user_service
from src.shared.infrastructure.dependencies import get_token_validation_service

class AuthController(BaseModel):
    sub: str
    email: str | None = None
    scope: str | None = None
    permissions: list[str] | None = []


router = APIRouter(prefix="/users-sync", tags=["UsersSync"])

@router.post("/upsert")
def upsert_user_from_action(
    body: AuthController,
    _: Dict[str, Any] = Depends(get_token_validation_service().require_role("sync:users")),
    service: UserService = Depends(get_user_service)
):
    payload = {
        "sub": body.sub,
        "email": body.email,
        "scope": body.scope or "",
        "permissions": body.permissions or []
    }
    user = service.get_or_create_from_payload(payload)
    return {"ok": True, "id": user.id}

@router.post("/sync")
def sync_user_from_token(
    payload: Dict[str, Any] = Depends(get_token_validation_service().verify_token),
    service: UserService = Depends(get_user_service)
):
    if "sub" not in payload:
        raise HTTPException(status_code=400, detail="Token payload is missing 'sub'")

    user = service.get_or_create_from_payload(payload)
    return {"ok": True, "id": user.id}

@router.get("/me")
def me(
    payload = Depends(get_token_validation_service().verify_token),
    service: UserService = Depends(get_user_service)
):
    user = service.get_or_create_from_payload(payload)
    return asdict(user)
