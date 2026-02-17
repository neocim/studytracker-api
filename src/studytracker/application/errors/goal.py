from uuid import UUID

from studytracker.domain.errors.base import app_error


@app_error
class InvalidPeriodRange:
    message: str = "Start period should be less than the end period"


@app_error
class ParentGoalNotFound:
    def __init__(self, goal_id: UUID) -> None:
        self._goal_id = goal_id

    @property
    def message(self) -> str:
        return f"Parent goal with id {self._goal_id} not found"
