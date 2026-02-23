from dataclasses import dataclass
from datetime import date
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.errors.goal import GoalNotFoundError
from studytracker.application.ports.data_context import DataContext
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class UpdateGoalRequest(Request[None]):
    goal_id: UUID
    name: str | None = None
    description: str | None = None
    period_start: date | None = None
    period_end: date | None = None
    is_success: bool | None = None


class UpdateGoalHandler(RequestHandler[UpdateGoalRequest, None]):
    def __init__(self, data_context: DataContext, goal_reader: GoalReader) -> None:
        self._data_context = data_context
        self._goal_reader = goal_reader

    @override
    async def handle(self, request: UpdateGoalRequest) -> None:
        goal = await self._goal_reader.get_by_id(request.goal_id)

        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        if request.name is not None:
            goal.name = request.name

        if request.description is not None:
            goal.description = request.description

        if request.period_start is not None:
            goal.period_start = request.period_start

        if request.period_end is not None:
            goal.period_end = request.period_end

        if request.is_success is not None:
            goal.is_success = request.is_success

        await self._data_context.commit()
