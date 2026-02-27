from dataclasses import dataclass
from datetime import date
from uuid import UUID

from studytracker.domain.entities.goal import GoalStatus


@dataclass(frozen=True)
class CreatedGoal:
    goal_id: UUID


@dataclass(frozen=True)
class GoalReadModel:
    user_id: UUID
    goal_id: UUID
    parent_id: UUID | None
    name: str
    description: str | None
    period_start: date
    period_end: date
    goal_status: GoalStatus


@dataclass(frozen=True)
class GoalWithSubgoalsReadModel:
    user_id: UUID
    goal_id: UUID
    parent_id: UUID | None
    name: str
    description: str | None
    period_start: date
    period_end: date
    goal_status: GoalStatus
    subgoals: list["GoalWithSubgoalsReadModel"]
