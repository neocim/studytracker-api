import logging
from uuid import UUID

from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from studytracker.api.dto.requests.goal import CreateGoal
from studytracker.api.dto.responses.goal import CreatedGoal, Goal
from studytracker.application.commands.create_goal import CreateGoalRequest
from studytracker.application.commands.create_subgoal import CreateSubgoalRequest
from studytracker.application.commands.delete_goal import DeleteGoalRequest
from studytracker.application.commands.update_goal import UpdateGoalRequest
from studytracker.application.queries.get_goal import GetGoalRequest

logger = logging.getLogger(__name__)

router = APIRouter(tags=["goals"], route_class=DishkaRoute, prefix="/users/{user_id}")


@router.post("/goals", status_code=status.HTTP_201_CREATED)
async def create_goal(
    user_id: UUID,
    sender: FromDishka[Sender],
    user_request: CreateGoal,
) -> CreatedGoal:
    logger.info("Request to create a goal")

    create_goal = CreateGoalRequest(
        user_id=user_id,
        name=user_request.name,
        period_start=user_request.period_start,
        period_end=user_request.period_end,
        description=user_request.description,
        goal_status=user_request.goal_status,
    )
    result = await sender.send(create_goal)
    logger.info("Goal created: %s", result.goal_id)

    return CreatedGoal(goal_id=result.goal_id)


@router.get("/goals/{goal_id}", status_code=status.HTTP_200_OK, name="get_goal")
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
        goal_status=result.goal_status,
    )


@router.patch("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_goal(
    goal_id: UUID,
    sender: FromDishka[Sender],
    name: str | None = None,
    description: str | None = None,
) -> None:
    logger.info("Request to update a goal")

    update_goal = UpdateGoalRequest(
        goal_id=goal_id,
        name=name,
        description=description,
    )
    await sender.send(update_goal)
    logger.info("Goal %s updated", goal_id)


@router.post("/goals/{parent_id}/subgoals", status_code=status.HTTP_201_CREATED)
async def create_subgoal(
    parent_id: UUID,
    user_id: UUID,
    sender: FromDishka[Sender],
    user_request: CreateGoal,
) -> CreatedGoal:
    logger.info("Request to create a subgoal")

    create_subgoal = CreateSubgoalRequest(
        user_id=user_id,
        name=user_request.name,
        parent_id=parent_id,
        period_start=user_request.period_start,
        period_end=user_request.period_end,
        goal_status=user_request.goal_status,
        description=user_request.description,
    )
    result = await sender.send(create_subgoal)
    logger.info("Subgoal created: %s", result.goal_id)

    return CreatedGoal(goal_id=result.goal_id)


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: UUID, sender: FromDishka[Sender]) -> None:
    logger.info("Request to delete a goal")

    delete_goal = DeleteGoalRequest(goal_id=goal_id)
    await sender.send(delete_goal)
    logger.info("Goal deleted")
