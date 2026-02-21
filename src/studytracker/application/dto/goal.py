from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreatedGoal:
    goal_id: UUID
