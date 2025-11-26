from fastapi import APIRouter, Depends, HTTPException, status

from src.notifications.application.notification_service import NotificationService
from src.notifications.infrastructure.dependencies import (
    get_notification_repository,
    get_notification_service,
)
from src.notifications.interfaces.dto import (
    NotificationRequestDTO,
    NotificationResponseDTO,
)


def _model_dump(model, **kwargs):
    """
    Helper compatible con Pydantic v1/v2 para extraer dict.
    """
    if hasattr(model, "model_dump"):
        return model.model_dump(**kwargs)
    return model.dict(**kwargs)


class NotificationController:
    def __init__(self):
        self.router = APIRouter(prefix="/notifications", tags=["Notifications"])
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.post(
            "",
            response_model=NotificationResponseDTO,
            status_code=status.HTTP_201_CREATED,
        )
        def create_notification(
            payload: NotificationRequestDTO,
            service: NotificationService = Depends(get_notification_service),
        ):
            try:
                data = _model_dump(payload, by_alias=False)
                notification = service.create_notification(**data)
                return NotificationResponseDTO.from_domain(notification)
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
                ) from exc

        @self.router.get(
            "",
            response_model=list[NotificationResponseDTO],
            status_code=status.HTTP_200_OK,
        )
        def list_notifications(
            service: NotificationService = Depends(get_notification_service),
        ):
            notifications = service.list_notifications()
            return [
                NotificationResponseDTO.from_domain(notification)
                for notification in notifications
            ]

        @self.router.get(
            "/{notification_id}",
            response_model=NotificationResponseDTO,
            status_code=status.HTTP_200_OK,
        )
        def get_notification(
            notification_id: str,
            service: NotificationService = Depends(get_notification_service),
        ):
            try:
                notification = service.get_notification(notification_id)
                return NotificationResponseDTO.from_domain(notification)
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc

        @self.router.get(
            "/user/{user_id}",
            response_model=list[NotificationResponseDTO],
            status_code=status.HTTP_200_OK,
        )
        def list_by_user(
            user_id: str,
            service: NotificationService = Depends(get_notification_service),
        ):
            notifications = service.list_by_user(user_id)
            return [
                NotificationResponseDTO.from_domain(notification)
                for notification in notifications
            ]

        @self.router.delete(
            "/{notification_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        def delete_notification(
            notification_id: str,
            service: NotificationService = Depends(get_notification_service),
        ):
            try:
                service.delete_notification(notification_id)
            except ValueError as exc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
                ) from exc
