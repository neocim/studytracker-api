from dataclasses import dataclass
from datetime import date
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.dto.goal import CreatedGoal
from studytracker.application.errors.goal import ParentGoalNotFoundError
from studytracker.application.ports.data_context import DataContext
from studytracker.application.ports.goal_mapper import GoalMapper
from studytracker.application.ports.id_generator import IDGenerator
from studytracker.domain.entities.goal import Goal, GoalStatus
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class CreateSubgoalRequest(Request[CreatedGoal]):
    user_id: UUID
    parent_id: UUID
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus | None = None
    description: str | None = None


class CreateSubgoalHandler(RequestHandler[CreateSubgoalRequest, CreatedGoal]):
    def __init__(
        self,
        goal_reader: GoalReader,
        data_context: DataContext,
        goal_mapper: GoalMapper,
        id_generator: IDGenerator,
    ) -> None:
        self._goal_reader = goal_reader
        self._data_context = data_context
        self._mapper = goal_mapper
        self._id_generator = id_generator

    @override
    async def handle(self, request: CreateSubgoalRequest) -> CreatedGoal:
        # Using a high depth value to get all subgoals, as the endpoint is not paginated.
        # This is bad practice
        goal = await self._goal_reader.get_with_subgoals(goal_id=request.parent_id, user_id=request.user_id, depth=1000)
        if goal is None:
            raise ParentGoalNotFoundError(goal_id=request.parent_id)

        subgoal_id = self._id_generator.get_uuid()

        new_subgoal: Goal = Goal(
            entity_id=subgoal_id,
            user_id=request.user_id,
            parent=goal,
            period_start=request.period_start,
            period_end=request.period_end,
            name=request.name,
            description=request.description,
            goal_status=request.goal_status,
        )

        goal.add_subgoal(new_subgoal)
        await self._data_context.commit()

        return self._mapper.to_created(new_subgoal)
