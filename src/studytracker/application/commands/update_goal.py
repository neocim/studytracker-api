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
    user_id: UUID
    goal_id: UUID
    name: str | None
    description: str | None
    period_start: date | None
    period_end: date | None


class UpdateGoalHandler(RequestHandler[UpdateGoalRequest, None]):
    def __init__(self, data_context: DataContext, goal_reader: GoalReader) -> None:
        self._data_context = data_context
        self._goal_reader = goal_reader

    @override
    async def handle(self, request: UpdateGoalRequest) -> None:
        goal = await self._goal_reader.get_by_id(goal_id=request.goal_id, user_id=request.user_id)
        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        if request.name is not None:
            goal.set_name(request.name)
        if request.description is not None:
            goal.set_description(request.description)
        goal.set_periods(request.period_start, request.period_end)

        await self._data_context.commit()
