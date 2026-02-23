import logging
from uuid import UUID

from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response, status

from studytracker.api.config import APIConfig
from studytracker.api.dto.requests.goal import CreateGoal
from studytracker.api.dto.responses.goal import CreatedGoal, Goal
from studytracker.application.commands.create_goal import CreateGoalRequest
from studytracker.application.queries.get_goal import GetGoalRequest

logger = logging.getLogger(__name__)

router = APIRouter(route_class=DishkaRoute, prefix="/users/{user_id}")


@router.post("/goals", status_code=status.HTTP_201_CREATED)
async def create_goal(
    user_id: UUID,
    sender: FromDishka[Sender],
    user_request: CreateGoal,
    request: Request,
    response: Response,
) -> CreatedGoal:
    logger.info("Request to create a goal")

    create_goal = CreateGoalRequest(
        user_id=user_id,
        name=user_request.name,
        period_start=user_request.period_start,
        period_end=user_request.period_end,
        parent_id=user_request.parent_id,
        description=user_request.description,
        is_success=user_request.is_success,
    )

    result = await sender.send(create_goal)
    logger.info("Goal created")

    response.headers["Location"] = request.url_for("get_goal", goal_id=result.goal_id, sender=sender).__str__()
    return CreatedGoal(goal_id=result.goal_id)

@router.get("/goals/{goal_id}", status_code=status.HTTP_200_OK)
async def get_goal(goal_id: UUID, sender: FromDishka[Sender]) -> Goal:
    get_goal = GetGoalRequest(goal_id=goal_id)
    result = await sender.send(get_goal)

    return Goal(
        goal_id=result.goal_id,
        user_id=result.user_id,
        name=result.name,
        description=result.description,
        period_start=result.period_start,
        period_end=result.period_end,
        parent_id=result.parent_id,
        is_success=result.is_success,
    )