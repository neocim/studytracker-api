from uuid import UUID

from studytracker.domain.errors.base import AppError, ErrorCode, app_error


@app_error
class InvalidPeriodRangeError(AppError):
    def __init__(self, goal_id: UUID) -> None:
        self._goal_id = goal_id
        super().__init__(code=ErrorCode.INVALID_PERIOD_RANGE, status_code=422)

    @property
    def message(self) -> str:
        return "Start period should be less than the end period"


@app_error
class ParentGoalNotFoundError(AppError):
    def __init__(self, goal_id: UUID) -> None:
        self._goal_id = goal_id
        super().__init__(code=ErrorCode.NOT_FOUND, status_code=404)

    @property
    def message(self) -> str:
        return f"Parent goal with id {self._goal_id} not found"
