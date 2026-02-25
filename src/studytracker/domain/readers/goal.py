from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from studytracker.domain.entities.goal import Goal


class GoalReader(Protocol):
    @abstractmethod
    async def get_by_id(self, goal_id: UUID, user_id: UUID) -> Goal | None:
        raise NotImplementedError

    @abstractmethod
    async def get_with_subgoals(self, goal_id: UUID, user_id: UUID) -> Goal | None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, goal_id: UUID) -> bool:
        raise NotImplementedError
