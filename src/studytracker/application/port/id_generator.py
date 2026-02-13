from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IDGenerator(Protocol):
    @abstractmethod
    def generate_goal_id() -> UUID:
        raise NotImplementedError
