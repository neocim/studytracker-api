import logging
from uuid import UUID

from bazario import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, status

from studytracker.api.dto.requests.goal import CreateGoal
from studytracker.api.dto.responses.goal import CreatedGoal
from studytracker.application.commands.create_goal import CreateGoalRequest

logger = logging.getLogger(__name__)

router = APIRouter(route_class=DishkaRoute, prefix="/users/{user_id}")


@router.post("/goals", status_code=status.HTTP_422)
async def create(user_id: UUID, sender: FromDishka[Sender], request: CreateGoal, response: Response) -> CreatedGoal:
    logger.info("Request to create a goal")

    result = await sender.send(
        CreateGoalRequest(
            user_id=user_id,
            name=request.name,
            period_start=request.period_start,
            period_end=request.period_end,
            parent_id=request.parent_id,
            description=request.description,
            is_success=request.is_success,
        ),
    )
