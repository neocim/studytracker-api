from datetime import date

from pydantic import BaseModel

from studytracker.domain.entities.goal import GoalStatus


class CreateGoal(BaseModel):
    name: str
    period_start: date
    period_end: date
    goal_status: GoalStatus | None
    description: str | None


class UpdateGoal(BaseModel):
    name: str | None
    description: str | None
