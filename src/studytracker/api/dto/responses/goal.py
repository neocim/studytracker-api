from uuid import UUID

from pydantic import BaseModel


class CreatedGoal(BaseModel):
    goal_id: UUID
