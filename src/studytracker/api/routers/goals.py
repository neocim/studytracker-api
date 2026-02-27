import logging
from datetime import date
from uuid import UUID

from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status
from pydantic import BaseModel

from studytracker.application.commands.create_goal import CreateGoalRequest
from studytracker.application.commands.create_subgoal import CreateSubgoalRequest
from studytracker.application.commands.delete_goal import DeleteGoalRequest
from studytracker.application.commands.set_status import SetGoalStatusRequest
from studytracker.application.commands.update_goal import UpdateGoalRequest
from studytracker.application.dto.goal import CreatedGoal, GoalReadModel, GoalWithSubgoalsReadModel
from studytracker.application.queries.get_goal import GetGoalRequest
from studytracker.application.queries.get_many_goals import GetManyGoalsRequest
from studytracker.application.queries.get_with_subgoals import GetGoalWithSubgoalsRequest
from studytracker.domain.entities.goal import GoalStatus

logger = logging.getLogger(__name__)

router = APIRouter(tags=["goals"], route_class=DishkaRoute, prefix="/users/{user_id}")


class CreateGoalBody(BaseModel):
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus | None
    description: str | None


class UpdateGoalBody(BaseModel):
    name: str | None
    description: str | None


@router.post("/goals", status_code=status.HTTP_201_CREATED)
async def create_goal(
    user_id: UUID,
    body: CreateGoalBody,
    sender: FromDishka[Sender],
) -> CreatedGoal:
    logger.info("Request to create a goal")
    create_goal = CreateGoalRequest(
        user_id=user_id,
        name=body.name,
        period_start=body.period_start,
        period_end=body.period_end,
        description=body.description,
        goal_status=body.goal_status,
    )
    result = await sender.send(create_goal)
    logger.info("Goal created")
    return result


@router.post("/goals/{parent_id}/subgoals", status_code=status.HTTP_201_CREATED)
async def create_subgoal(
    user_id: UUID,
    parent_id: UUID,
    body: CreateGoalBody,
    sender: FromDishka[Sender],
) -> CreatedGoal:
    logger.info("Request to create a subgoal")

    create_subgoal = CreateSubgoalRequest(
        user_id=user_id,
        name=body.name,
        parent_id=parent_id,
        period_start=body.period_start,
        period_end=body.period_end,
        goal_status=body.goal_status,
        description=body.description,
    )
    result = await sender.send(create_subgoal)
    logger.info("Subgoal created")
    return result


@router.get("/goals/{goal_id}", status_code=status.HTTP_200_OK)
async def get_goal(
    user_id: UUID,
    goal_id: UUID,
    sender: FromDishka[Sender],
) -> GoalReadModel:
    get_goal = GetGoalRequest(goal_id=goal_id, user_id=user_id)
    result = await sender.send(get_goal)
    return result


@router.get("/goals/{goal_id}/subgoals", status_code=status.HTTP_200_OK)
async def get_with_subgoals(
    user_id: UUID,
    goal_id: UUID,
    sender: FromDishka[Sender],
) -> GoalWithSubgoalsReadModel:
    get_goal = GetGoalWithSubgoalsRequest(goal_id=goal_id, user_id=user_id)
    result = await sender.send(get_goal)
    return result


@router.get("/goals", status_code=status.HTTP_200_OK)
async def get_many_goals(
    user_id: UUID,
    sender: FromDishka[Sender],
) -> list[GoalReadModel]:
    get_goals = GetManyGoalsRequest(user_id=user_id)
    result = await sender.send(get_goals)
    return result


@router.patch("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_goal(
    user_id: UUID,
    goal_id: UUID,
    body: UpdateGoalBody,
    sender: FromDishka[Sender],
) -> None:
    logger.info("Request to update a goal")

    update_goal = UpdateGoalRequest(
        user_id=user_id,
        goal_id=goal_id,
        name=body.name,
        description=body.description,
    )
    await sender.send(update_goal)
    logger.info("Goal updated")


@router.patch("/goals/{goal_id}/{status}", status_code=status.HTTP_204_NO_CONTENT)
async def set_status(user_id: UUID, goal_id: UUID, status: GoalStatus, sender: FromDishka[Sender]) -> None:
    logger.info("Request to set %s status for goal", status)

    set_status = SetGoalStatusRequest(user_id=user_id, goal_id=goal_id, status=status)
    await sender.send(set_status)
    logger.info("%s status has been set", status)


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(user_id: UUID, goal_id: UUID, sender: FromDishka[Sender]) -> None:
    logger.info("Request to delete a goal")

    delete_goal = DeleteGoalRequest(goal_id=goal_id, user_id=user_id)
    await sender.send(delete_goal)
    logger.info("Goal deleted")
