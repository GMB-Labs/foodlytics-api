from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status,Response

from src.profile.domain.model.commands.create_profile_command import CreateProfileCommand
from src.profile.domain.model.commands.update_profile_command import UpdateProfileCommand
from src.profile.domain.model.commands.update_profile_picture_command import UpdateProfilePictureCommand
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.domain.services.profile_command_service import ProfileCommandService
from src.profile.infrastructure.dependencies import (get_profile_command_service,get_profile_repository,)
from src.profile.interfaces.dto.profile_dto import ProfileResponseDTO
from src.profile.interfaces.dto.create_profile_request_dto import CreateProfileDTO
from src.profile.interfaces.dto.update_profile_request_dto import UpdateProfileDTO

def _model_dump(model, **kwargs):
    """
    Helper compatible with Pydantic v1/v2 to extract dict data.
    """
    if hasattr(model, "model_dump"):
        return model.model_dump(**kwargs)
    return model.dict(**kwargs)


class ProfileController:
    def __init__(self):
        self.router = APIRouter(prefix="/profiles", tags=["Profiles"])
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.post(
            "",
            status_code=status.HTTP_201_CREATED,
            response_model=ProfileResponseDTO,
        )
        def create_profile(
            payload: CreateProfileDTO,
            service: ProfileCommandService = Depends(get_profile_command_service),
        ):
            try:
                command = CreateProfileCommand.from_primitives(**_model_dump(payload))
                profile = service.create_profile(command)
                return ProfileResponseDTO.from_domain(profile)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

        @self.router.put(
            "/{user_id}",
            response_model=ProfileResponseDTO,
        )
        def update_profile(
            user_id: str,
            payload: UpdateProfileDTO,
            service: ProfileCommandService = Depends(get_profile_command_service),
        ):
            update_data = _model_dump(payload, exclude_unset=True, exclude_none=True)
            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="At least one field must be provided to update the profile.",
                )
            try:
                command = UpdateProfileCommand.from_primitives(user_id=user_id, **update_data)
                profile = service.update_profile(command)
                return ProfileResponseDTO.from_domain(profile)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        @self.router.patch(
            "/{user_id}/picture",
            response_model=ProfileResponseDTO,
        )
        async def update_profile_picture(
            user_id: str,
            file: UploadFile = File(...),
            service: ProfileCommandService = Depends(get_profile_command_service),
        ):
            data = await file.read()
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image file cannot be empty.",
                )
            try:
                command = UpdateProfilePictureCommand(
                    profile_id=user_id,
                    picture_data=data,
                    picture_mime_type=file.content_type or "application/octet-stream",
                )
                profile = service.update_profile_picture(command)
                return ProfileResponseDTO.from_domain(profile)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


        @self.router.get(
            "/{user_id}",
            response_model=ProfileResponseDTO,
        )
        def get_profile(
            user_id: str,
            repository: ProfileRepository = Depends(get_profile_repository),
        ):
            profile = repository.find_by_user_id(user_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found.",
                )
            return ProfileResponseDTO.from_domain(profile)

        @self.router.get(
            "",
            response_model=List[ProfileResponseDTO],
        )
        def list_profiles(
            repository: ProfileRepository = Depends(get_profile_repository),
        ):
            profiles = repository.list_all()
            return [ProfileResponseDTO.from_domain(profile) for profile in profiles]

        @self.router.get(
            "/patients/{nutritionist_id}",
            response_model=List[ProfileResponseDTO],
        )
        def list_by_nutritionist(
            nutritionist_id: str,
            repository: ProfileRepository = Depends(get_profile_repository),
        ):
            profiles = repository.find_patient_profile_by_nutritionist_id(nutritionist_id)
            return [ProfileResponseDTO.from_domain(profile) for profile in profiles]

        @self.router.delete(
            "/{user_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        def delete_profile(
            user_id: str,
            service: ProfileCommandService = Depends(get_profile_command_service),
        ):
            try:
                service.delete_profile(user_id)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        @self.router.get("/{user_id}/picture")
        def get_profile_picture(
                user_id: str,
                repository: ProfileRepository = Depends(get_profile_repository),
        ):
            profile = repository.find_by_user_id(user_id)
            if not profile:
                raise HTTPException(status_code=404, detail="Profile not found.")
            picture = profile.profile_picture
            if not picture:
                raise HTTPException(status_code=404, detail="Profile has no picture.")
            return Response(
                content=picture.image_data,
                media_type=picture.mime_type,
                headers={"Content-Disposition": f'inline; filename="{user_id}.img"'},
            )