import uuid
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.errors.goal import InvalidPeriodRange, ParentGoalNotFound
from studytracker.application.ports.data_context import DataContext
from studytracker.application.queries.gateways.goal import GoalGateway
from studytracker.domain.entities.goal import Goal


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
    def __init__(self, goal_gateway: GoalGateway, data_context: DataContext) -> None:
        self._goal_gateway = goal_gateway
        self._data_context = data_context

    async def handle(self, request: CreateGoalRequest) -> None:
        if request.period_start >= request.period_end:
            raise InvalidPeriodRange

        if request.parent_id is not None and not self._goal_gateway.exists(request.parent_id):
            raise ParentGoalNotFound

        goal_id = uuid.uuid4()
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
        self._data_context.commit()
