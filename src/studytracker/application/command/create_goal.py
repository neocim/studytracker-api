from dataclasses import dataclass
from datetime import date
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.ports.id_generator import IDGenerator
from studytracker.domain.repository.goal_repository import GoalRepository


@dataclass(frozen=True)
class CreateGoalRequest(Request[None]):
    id: UUID
    user_id: UUID
    period_start: date
    period_end: date
    name: str
    description: str | None = None
    is_success: bool | None = None

class CreateGoalRequestHandler(RequestHandler[CreateGoalRequest, None]):
    def __init__(self, id_generator: IDGenerator, goal_repository: GoalRepository) -> None:
        

    async def handle(self, request: CreateGoalRequest) -> None:
        
