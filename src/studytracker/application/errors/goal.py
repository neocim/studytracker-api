from typing import ClassVar
from uuid import UUID

from studytracker.domain.errors.base import AppError, app_error


@app_error
class InvalidPeriodRangeError(AppError):
    code: ClassVar[str] = "UNPROCESSABLE_ENTITY"

    @property
    def message(self) -> str:
        return "Start period should be less than the end period"


@app_error
class ParentGoalNotFoundError(AppError):
    code: ClassVar[str] = "NOT_FOUND"
    goal_id: UUID

    @property
    def message(self) -> str:
        return f"Parent goal with id {self.goal_id} not found"
