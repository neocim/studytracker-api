from dataclasses import dataclass
from datetime import date
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.errors.goal import GoalNotFound, InvalidPeriodRange
from studytracker.application.query.gateway.goal import GoalGateway
from studytracker.domain.repository.goal_repository import GoalRepository


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
    def __init__(self, goal_gateway: GoalGateway, goal_repository: GoalRepository) -> None:
        self._goal_gateway = goal_gateway
        self._goal_repository = goal_repository

    async def handle(self, request: CreateGoalRequest) -> None:
        if request.period_start >= request.period_end:
            raise InvalidPeriodRange

        if request.parent_id is not None and not self._goal_gateway.exists(request.parent_id):
            raise GoalNotFound
