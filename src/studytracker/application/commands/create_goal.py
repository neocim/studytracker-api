from dataclasses import dataclass
from datetime import date
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.errors.goal import InvalidPeriodRangeError, ParentGoalNotFoundError
from studytracker.application.ports.data_context import DataContext
from studytracker.application.ports.id_generator import IDGenerator
from studytracker.domain.entities.goal import Goal
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class CreateGoalRequest(Request[None]):
    user_id: UUID
    period_start: date
    period_end: date
    name: str
    parent_id: UUID | None = None
    description: str | None = None
    is_success: bool | None = None


class CreateGoalHandler(RequestHandler[CreateGoalRequest, None]):
    def __init__(self, goal_reader: GoalReader, data_context: DataContext, id_generator: IDGenerator) -> None:
        self._goal_reader = goal_reader
        self._data_context = data_context
        self._id_generator = id_generator

    async def handle(self, request: CreateGoalRequest) -> None:
        if request.period_start >= request.period_end:
            raise InvalidPeriodRangeError

        goal_exists = await self._goal_reader.exists(request.parent_id)

        if request.parent_id is not None and not goal_exists:
            raise ParentGoalNotFoundError

        goal_id = self._id_generator.get_uuid()
        new_goal = (
            Goal(
                entity_id=goal_id,
                user_id=request.user_id,
                period_start=request.period_start,
                period_end=request.period_end,
                name=request.name,
                description=request.description,
                parent_id=request.parent_id,
                is_success=request.is_success,
            ),
        )

        self._data_context.goal_repository.add(new_goal)
        await self._data_context.commit()
