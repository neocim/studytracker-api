from dataclasses import dataclass
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.errors.goal import GoalNotFoundError
from studytracker.application.ports.data_context import DataContext
from studytracker.domain.entities.goal import GoalStatus
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class SetGoalStatusRequest(Request[None]):
    user_id: UUID
    goal_id: UUID
    status: GoalStatus


class SetGoalStatusHandler(RequestHandler[SetGoalStatusRequest, None]):
    def __init__(self, data_context: DataContext, goal_reader: GoalReader) -> None:
        self._data_context = data_context
        self._goal_reader = goal_reader

    @override
    async def handle(self, request: SetGoalStatusRequest) -> None:
        goal = await self._goal_reader.get_by_id(goal_id=request.goal_id, user_id=request.user_id)
        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        goal.set_status(request.status)
        await self._data_context.commit()
