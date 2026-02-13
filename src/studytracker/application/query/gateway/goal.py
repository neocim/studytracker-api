from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

@dataclass(frozen=True)
class GoalReadModel:

class GoalGateway(Protocol):
    @abstractmethod
    def get_by_id(self, id: UUID) -> GoalReadModel:
