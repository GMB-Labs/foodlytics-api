import random
from typing import Optional

from src.profile.domain.model.aggregates.profile import Profile
from src.profile.domain.model.entities.nutritionist_invite_code import NutritionistInviteCode
from src.profile.domain.repositories.nutritionist_invite_code_repository import (
    NutritionistInviteCodeRepository,
)
from src.profile.domain.repositories.profile_repository import ProfileRepository


class NutritionistInviteService:
    """
    Permite a un nutricionista generar códigos y a un paciente usarlos para asociarse.
    """

    def __init__(
        self,
        code_repository: NutritionistInviteCodeRepository,
        profile_repository: ProfileRepository,
        max_attempts: int = 5,
    ):
        self.code_repository = code_repository
        self.profile_repository = profile_repository
        self.max_attempts = max_attempts

    def _generate_unique_code(self) -> str:
        for _ in range(self.max_attempts):
            code = f"{random.randint(0, 999999):06d}"
            if not self.code_repository.find_by_code(code):
                return code
        raise RuntimeError("No se pudo generar un código único, intente nuevamente.")

    def generate_code(self, *, nutritionist_id: str) -> NutritionistInviteCode:
        existing = self.code_repository.find_active_by_nutritionist(nutritionist_id)
        if existing:
            return existing

        code_value = self._generate_unique_code()
        code = NutritionistInviteCode.create(code=code_value, nutritionist_id=nutritionist_id)
        return self.code_repository.save(code)

    def _get_patient_profile(self, patient_id: str) -> Profile:
        profile = self.profile_repository.find_by_user_id(patient_id)
        if not profile:
            raise ValueError("Profile not found for patient.")
        return profile

    def redeem_code(self, *, code: str, patient_id: str) -> Profile:
        invite = self.code_repository.find_by_code(code)
        if not invite:
            raise ValueError("Código inválido.")
        if invite.used:
            raise ValueError("Código ya fue usado.")

        profile = self._get_patient_profile(patient_id)
        if profile.nutritionist_id:
            raise ValueError("El paciente ya tiene un nutricionista asignado.")

        profile.nutritionist_id = invite.nutritionist_id
        invite.mark_used(patient_id)

        self.profile_repository.save(profile)
        self.code_repository.save(invite)
        return profile
