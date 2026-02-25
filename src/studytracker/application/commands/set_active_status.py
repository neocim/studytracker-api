from dataclasses import dataclass
from typing import override

from bazario import Request
from bazario.asyncio import RequestHandler
from sqlalchemy import UUID

from studytracker.application.errors.goal import GoalNotFoundError
from studytracker.application.ports.data_context import DataContext
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class SetActiveGoalStatusRequest(Request[None]):
    user_id: UUID
    goal_id: UUID


class SetActiveGoalStatusHandler(RequestHandler(SetActiveGoalStatusRequest, None)):
    def __init__(self, data_context: DataContext, goal_reader: GoalReader) -> None:
        self._data_context = data_context
        self._goal_reader = goal_reader

    @override
    async def handle(self, request: SetActiveGoalStatusRequest) -> None:
        goal = await self._goal_reader.get_by_id(request.goal_id, request.user_id)
        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        goal.try_set_active_status()
        await self._data_context.commit()
