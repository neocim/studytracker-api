from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class CreatedGoal:
    goal_id: UUID


@dataclass(frozen=True)
class GoalReadModel:
    goal_id: UUID
    user_id: UUID
    name: str
    period_start: date
    period_end: date
    description: str | None
    parent_id: UUID | None
    is_success: bool | None
