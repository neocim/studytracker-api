from typing import ClassVar, override

from studytracker.domain.errors.base import AppError, app_error


@app_error
class InvalidPeriodRangeError(AppError):
    code: ClassVar[str] = "INVALID_PERIOD_RANGE"

    @override
    @property
    def message(self) -> str:
        return "Start period should be less than the end period"


@app_error
class InvalidStatusForCompletedGoalError(AppError):
    code: ClassVar[str] = "INVALID_STATUS"

    @override
    @property
    def message(self) -> str:
        return "Only SUCCEEDED, FAILED, or CANCELED statuses are allowed for completed goals"


@app_error
class InvalidStatusForNotStartedGoalError(AppError):
    code: ClassVar[str] = "INVALID_STATUS"

    @override
    @property
    def message(self) -> str:
        return "Only PENDING or CANCELED statuses are allowed for not started goals"
