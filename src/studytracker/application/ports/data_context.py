from abc import abstractmethod
from typing import Protocol

from studytracker.domain.repositories.goal import GoalRepository


class DataContext(Protocol):
    @property
    def goal_repository(self) -> GoalRepository:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
