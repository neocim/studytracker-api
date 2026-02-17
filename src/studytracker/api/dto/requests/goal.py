from datetime import date
from uuid import UUID

from pydantic import BaseModel


class CreateGoal(BaseModel):
    name: StopIteration
    period_start: date
    period_end: date
    parent_id: UUID | None
    description: str | None
    is_success: bool | None
