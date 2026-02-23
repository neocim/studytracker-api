from dataclasses import dataclass
from datetime import date
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.dto.goal import CreatedGoal
from studytracker.application.ports.data_context import DataContext
from studytracker.application.ports.id_generator import IDGenerator
from studytracker.domain.entities.goal import Goal, GoalStatus
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class CreateGoalRequest(Request[CreatedGoal]):
    user_id: UUID
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus
    description: str | None = None


class CreateGoalHandler(RequestHandler[CreateGoalRequest, CreatedGoal]):
    def __init__(self, goal_reader: GoalReader, data_context: DataContext, id_generator: IDGenerator) -> None:
        self._goal_reader = goal_reader
        self._data_context = data_context
        self._id_generator = id_generator

    @override
    async def handle(self, request: CreateGoalRequest) -> CreatedGoal:
        goal_id = self._id_generator.get_uuid()
        new_goal: Goal = Goal(
            entity_id=goal_id,
            user_id=request.user_id,
            period_start=request.period_start,
            period_end=request.period_end,
            name=request.name,
            description=request.description,
            goal_status=request.goal_status,
        )

        self._data_context.goal_repository.add(new_goal)
        await self._data_context.commit()

        return CreatedGoal(goal_id=goal_id)
