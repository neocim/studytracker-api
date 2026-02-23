from datetime import date
from uuid import UUID

from pydantic import BaseModel

from studytracker.domain.entities.goal import GoalStatus


class CreatedGoal(BaseModel):
    goal_id: UUID


class Goal(BaseModel):
    goal_id: UUID
    user_id: UUID
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus
    parent_id: UUID | None = None
    description: str | None = None
