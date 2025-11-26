from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Response

from src.profile.domain.model.commands.update_profile_command import UpdateProfileCommand
from src.profile.domain.model.commands.update_profile_picture_command import UpdateProfilePictureCommand
from src.profile.domain.repositories.profile_repository import ProfileRepository
from src.profile.application.internal.commandservices.profile_command_service import ProfileCommandService
from src.profile.application.internal.services.nutritionist_invite_service import NutritionistInviteService
from src.profile.infrastructure.dependencies import (
    get_profile_command_service,
    get_profile_repository,
    get_nutritionist_invite_service,
)
from src.profile.interfaces.dto.profile_dto import ProfileResponseDTO
from src.profile.interfaces.dto.user_registered_event_dto import UserRegisteredEventDTO
from src.profile.interfaces.dto.update_profile_request_dto import UpdateProfileDTO
from src.profile.interfaces.dto.nutritionist_invite_dto import (
    GenerateInviteResponseDTO,
    RedeemInviteRequestDTO,
    NutritionistInfoResponseDTO,
)
from src.shared.infrastructure.dependencies import get_event_bus
from src.shared.domain.events.event_bus import EventBus
from src.iam.domain.events.user_registered_event import UserRegisteredEvent
from src.iam.domain.model.value_objects.user_role import UserRole

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

        @self.router.put("/{user_id}",  response_model=ProfileResponseDTO )
        def update_profile( user_id: str, payload: UpdateProfileDTO, service: ProfileCommandService = Depends(get_profile_command_service) ):
            update_data = _model_dump(payload, exclude_unset=True, exclude_none=True)
            if not update_data:
                raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field must be provided to update the profile." )
            try:
                command = UpdateProfileCommand.from_primitives(user_id=user_id, **update_data)
                profile = service.update_profile(command)
                return ProfileResponseDTO.from_domain(profile)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        @self.router.patch("/{user_id}/picture",response_model=ProfileResponseDTO)
        async def update_profile_picture(user_id: str,file: UploadFile = File(...),service: ProfileCommandService = Depends(get_profile_command_service) ):
            data = await file.read()
            if not data:
                raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Image file cannot be empty." )
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



        @self.router.get("/{user_id}",response_model=ProfileResponseDTO)
        def get_profile(user_id: str,repository: ProfileRepository = Depends(get_profile_repository) ):
            profile = repository.find_by_user_id(user_id)
            if not profile:
                raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,detail="Profile not found." )
            return ProfileResponseDTO.from_domain(profile)


        @self.router.get("",response_model=List[ProfileResponseDTO],summary="TESTING" )
        def list_profiles( repository: ProfileRepository = Depends(get_profile_repository) ):
            """
            Testing endpoint to list all profiles (not for production use)
            """
            profiles = repository.list_all()
            return [ProfileResponseDTO.from_domain(profile) for profile in profiles]


        @self.router.get( "/patients/{nutritionist_id}",response_model=List[ProfileResponseDTO])
        def list_by_nutritionist(nutritionist_id: str,repository: ProfileRepository = Depends(get_profile_repository) ):
            profiles = repository.find_patient_profile_by_nutritionist_id(nutritionist_id)
            return [ProfileResponseDTO.from_domain(profile) for profile in profiles]


        @self.router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_profile(user_id: str, service: ProfileCommandService = Depends(get_profile_command_service),):
            try:
                service.delete_profile(user_id)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        @self.router.get("/{user_id}/picture")
        def get_profile_picture(user_id: str,repository: ProfileRepository = Depends(get_profile_repository) ):
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

        @self.router.post(
            "/nutritionists/{nutritionist_id}/invite-code",
            response_model=GenerateInviteResponseDTO,
            summary="Generates a code to invite patients to associate with the nutritionist",
        )
        def generate_invite_code(
            nutritionist_id: str,
            service: NutritionistInviteService = Depends(get_nutritionist_invite_service),
        ):
            code = service.generate_code(nutritionist_id=nutritionist_id)
            return {"code": code.code}

        @self.router.post(
            "/redeem-invite",
            response_model=NutritionistInfoResponseDTO,
            summary="Redeems an invite code for a patient to associate with a nutritionist",
        )
        def redeem_invite(
            payload: RedeemInviteRequestDTO,
            service: NutritionistInviteService = Depends(get_nutritionist_invite_service),
            profile_repo: ProfileRepository = Depends(get_profile_repository),
        ):
            try:
                profile = service.redeem_code(code=payload.code, patient_id=payload.patient_id)
                nutritionist_profile = (
                    profile_repo.find_by_user_id(profile.nutritionist_id) if profile.nutritionist_id else None
                )
                if not nutritionist_profile:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Nutritionist profile not found.",
                    )
                return NutritionistInfoResponseDTO(
                    first_name=nutritionist_profile.first_name,
                    last_name=nutritionist_profile.last_name,
                )
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
