from collections.abc import Sequence
from dataclasses import dataclass
from typing import override
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from studytracker.application.dto.goal import GoalReadModel
from studytracker.application.ports.goal_mapper import GoalMapper
from studytracker.domain.readers.goal import GoalReader


@dataclass(frozen=True)
class GetManyGoalsRequest(Request[list[GoalReadModel]]):
    user_id: UUID


class GetManyGoalsHandler(RequestHandler[GetManyGoalsRequest, Sequence[GoalReadModel]]):
    def __init__(self, goal_reader: GoalReader, goal_mapper: GoalMapper) -> None:
        self._goal_reader = goal_reader
        self._mapper = goal_mapper

    @override
    async def handle(self, request: GetManyGoalsRequest) -> Sequence[GoalReadModel]:
        goals = await self._goal_reader.get_many(user_id=request.user_id)
        return [self._mapper.to_readmodel(goal) for goal in goals]
