from dataclasses import dataclass
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.errors.goal import GoalNotFoundError
from studytracker.application.ports.data_context import DataContext
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class DeleteGoalRequest(Request[None]):
    user_id: UUID
    goal_id: UUID


class DeleteGoalHandler(RequestHandler[DeleteGoalRequest, None]):
    def __init__(self, data_context: DataContext, goal_reader: GoalReader) -> None:
        self._data_context = data_context
        self._goal_reader = goal_reader

    @override
    async def handle(self, request: DeleteGoalRequest) -> None:
        goal = await self._goal_reader.get_by_id(goal_id=request.goal_id, user_id=request.user_id)
        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        await self._data_context.goal_repository.delete(goal)
        await self._data_context.commit()
