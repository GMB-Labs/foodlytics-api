from abc import ABC, abstractmethod
from typing import Optional,List
from src.shared.domain.repositories.base_repository import BaseRepository
from src.profile.domain.model.aggregates.profile import Profile

class ProfileRepository(BaseRepository[Profile],ABC ):

    @abstractmethod
    def save(self,profile:Profile) -> None:
        """
        Save a profile.
        :param profile:
        :return:
        """
        pass


    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Optional[Profile]:
        """
        Find a profile by user ID.
        :param user_id:
        :return:
        """
        pass

    @abstractmethod
    def find_patient_profile_by_nutritionist_id(self, nutritionist_id: str) -> List[Profile]:
        """
        Find patient profiles by nutritionist ID.
        :param nutritionist_id:
        :return:
        """
        pass
