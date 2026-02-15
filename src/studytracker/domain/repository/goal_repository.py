from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from studytracker.domain.entity.goal import Goal


class GoalRepository(Protocol):
    @abstractmethod
    def add(self, goal: Goal) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove(self, goal: Goal) -> None:
        raise NotImplementedError
