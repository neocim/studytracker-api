from dataclasses import dataclass
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.dto.goal import GoalReadModel
from studytracker.application.errors.goal import GoalNotFoundError
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class GetGoalRequest(Request[GoalReadModel]):
    user_id: UUID
    goal_id: UUID


class GetGoalHandler(RequestHandler[GetGoalRequest, GoalReadModel]):
    def __init__(self, goal_reader: GoalReader) -> None:
        self._goal_reader = goal_reader

    @override
    async def handle(self, request: GetGoalRequest) -> GoalReadModel:
        goal = await self._goal_reader.get_by_id(goal_id=request.goal_id, user_id=request.user_id)
        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        return GoalReadModel(
            goal_id=goal.entity_id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            period_start=goal.period_start,
            period_end=goal.period_end,
            parent_id=goal.parent_id,
            goal_status=goal.goal_status,
        )
