from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.nutritionist_webtools.application.internal.commandservices.task_command_service import (
    TaskCommandService,
)
from src.nutritionist_webtools.application.internal.commandservices.calendar_event_command_service import (
    CalendarEventCommandService,
)
from src.nutritionist_webtools.domain.model.value_objects.task_status import TaskStatus
from src.nutritionist_webtools.infrastructure.dependencies import (
    get_task_command_service,
    get_calendar_event_command_service,
)
from src.nutritionist_webtools.interfaces.dto.task_dto import (
    TaskRequestDTO,
    TaskResponseDTO,
    TaskMoveRequestDTO,
)
from src.nutritionist_webtools.interfaces.dto.calendar_event_dto import (
    CalendarEventRequestDTO,
    CalendarEventResponseDTO,
)


class NutritionistWebtoolsController:
    def __init__(self):
        self.router = APIRouter(prefix="/nutritionists", tags=["Nutritionist Webtools"])
        self.register_routes()

    def register_routes(self) -> None:
        @self.router.post(
            "/{nutritionist_id}/tasks",
            response_model=TaskResponseDTO,
            status_code=status.HTTP_201_CREATED,
        )
        def create_task(
            nutritionist_id: str,
            payload: TaskRequestDTO,
            service: TaskCommandService = Depends(get_task_command_service),
        ):
            task = service.create_task(
                nutritionist_id=nutritionist_id,
                task_name=payload.task_name,
                task_description=payload.task_description,
                status=payload.status,
                deadline_date=payload.deadline_date,
            )
            return TaskResponseDTO.from_domain(task)

        @self.router.get(
            "/{nutritionist_id}/tasks",
            response_model=List[TaskResponseDTO],
        )
        def list_tasks(
            nutritionist_id: str,
            service: TaskCommandService = Depends(get_task_command_service),
        ):
            tasks = service.list_tasks(nutritionist_id=nutritionist_id)
            return [TaskResponseDTO.from_domain(task) for task in tasks]

        @self.router.delete(
            "/{nutritionist_id}/tasks/{task_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        def delete_task(
            nutritionist_id: str,  # kept for route consistency
            task_id: str,
            service: TaskCommandService = Depends(get_task_command_service),
        ):
            try:
                service.delete_task(task_id=task_id)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        @self.router.patch(
            "/{nutritionist_id}/tasks/{task_id}/move",
            response_model=TaskResponseDTO,
        )
        def move_task(
            nutritionist_id: str,  # kept for route consistency
            task_id: str,
            payload: TaskMoveRequestDTO,
            service: TaskCommandService = Depends(get_task_command_service),
        ):
            try:
                task = service.move_task(task_id=task_id, status=payload.status)
                return TaskResponseDTO.from_domain(task)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        @self.router.post(
            "/{nutritionist_id}/calendar-events",
            response_model=CalendarEventResponseDTO,
            status_code=status.HTTP_201_CREATED,
        )
        def create_calendar_event(
            nutritionist_id: str,
            payload: CalendarEventRequestDTO,
            service: CalendarEventCommandService = Depends(get_calendar_event_command_service),
        ):
            event = service.create_event(
                nutritionist_id=nutritionist_id,
                event_name=payload.event_name,
                event_date=payload.event_date,
                event_time=payload.event_time,
            )
            return CalendarEventResponseDTO.from_domain(event)

        @self.router.get(
            "/{nutritionist_id}/calendar-events",
            response_model=List[CalendarEventResponseDTO],
        )
        def list_calendar_events(
            nutritionist_id: str,
            service: CalendarEventCommandService = Depends(get_calendar_event_command_service),
        ):
            events = service.list_events(nutritionist_id=nutritionist_id)
            return [CalendarEventResponseDTO.from_domain(event) for event in events]

        @self.router.delete(
            "/{nutritionist_id}/calendar-events/{event_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        def delete_calendar_event(
            nutritionist_id: str,  # kept for route consistency
            event_id: str,
            service: CalendarEventCommandService = Depends(get_calendar_event_command_service),
        ):
            try:
                service.delete_event(event_id=event_id)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
