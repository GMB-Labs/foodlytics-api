from abc import ABC, abstractmethod
from typing import Optional

from src.profile.domain.model.entities.nutritionist_invite_code import NutritionistInviteCode


class NutritionistInviteCodeRepository(ABC):
    @abstractmethod
    def save(self, code: NutritionistInviteCode) -> NutritionistInviteCode:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[NutritionistInviteCode]:
        raise NotImplementedError

    @abstractmethod
    def find_active_by_nutritionist(self, nutritionist_id: str) -> Optional[NutritionistInviteCode]:
        """Return an unused code for the nutritionist if exists."""
        raise NotImplementedError
