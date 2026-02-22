from datetime import date
from uuid import UUID

from pydantic import BaseModel


class CreatedGoal(BaseModel):
    goal_id: UUID


class Goal(BaseModel):
    goal_id: UUID
    user_id: UUID
    period_start: date
    period_end: date
    name: str
    parent_id: UUID | None = None
    description: str | None = None
    is_success: bool | None = None
