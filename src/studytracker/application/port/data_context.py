from abc import abstractmethod
from typing import Protocol

from studytracker.domain.repository.goal_repository import GoalRepository


class DataContext(Protocol):
    goal_repository: GoalRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError