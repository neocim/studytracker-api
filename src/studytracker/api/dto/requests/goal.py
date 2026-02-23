from datetime import date
from uuid import UUID

from pydantic import BaseModel

from studytracker.domain.entities.goal import GoalStatus


class CreateGoal(BaseModel):
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus
    parent_id: UUID | None
    description: str | None
