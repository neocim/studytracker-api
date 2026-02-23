from typing import ClassVar, override
from uuid import UUID

from studytracker.domain.errors.base import AppError, app_error


@app_error
class ParentGoalNotFoundError(AppError):
    code: ClassVar[str] = "NOT_FOUND"
    goal_id: UUID

    @override
    @property
    def message(self) -> str:
        return f"Parent goal with id {self.goal_id} not found"


@app_error
class GoalNotFoundError(AppError):
    code: ClassVar[str] = "NOT_FOUND"
    goal_id: UUID

    @override
    @property
    def message(self) -> str:
        return f"Goal with id {self.goal_id} not found"
