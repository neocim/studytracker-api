from dataclasses import dataclass
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.dto.goal import GoalWithSubgoalsReadModel
from studytracker.application.errors.goal import GoalNotFoundError
from studytracker.application.ports.goal_mapper import GoalMapper
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class GetGoalWithSubgoalsRequest(Request[GoalWithSubgoalsReadModel]):
    user_id: UUID
    goal_id: UUID


class GetGoalWithSubgoalsHandler(RequestHandler[GetGoalWithSubgoalsRequest, GoalWithSubgoalsReadModel]):
    def __init__(self, goal_reader: GoalReader, goal_mapper: GoalMapper) -> None:
        self._goal_reader = goal_reader
        self._mapper = goal_mapper

    @override
    async def handle(self, request: GetGoalWithSubgoalsRequest) -> GoalWithSubgoalsReadModel:
        goal = await self._goal_reader.get_with_subgoals(goal_id=request.goal_id, user_id=request.user_id, depth=1000)
        if goal is None:
            raise GoalNotFoundError(goal_id=request.goal_id)

        return self._mapper.to_readmodel_with_subgoals(goal)
