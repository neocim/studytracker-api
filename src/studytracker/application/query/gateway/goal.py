from abc import abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class GoalReadModel:
    id: UUID
    user_id: UUID
    period_start: date
    period_end: date
    name: str
    parent_id: UUID | None
    description: str | None
    is_success: bool | None


class GoalGateway(Protocol):
    @abstractmethod
    def get_by_id(self, id: UUID) -> GoalReadModel:
        raise NotImplementedError
