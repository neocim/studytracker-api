from dataclasses import dataclass
from datetime import date
from uuid import UUID

from studytracker.domain.entities.goal import GoalStatus


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
    goal_status: GoalStatus
    parent_id: UUID | None
    description: str | None


@dataclass(frozen=True)
class GoalWithSubgoalsReadModel:
    goal_id: UUID
    user_id: UUID
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus
    subgoals: list["GoalWithSubgoalsReadModel"]
    parent_id: UUID | None
    description: str | None
