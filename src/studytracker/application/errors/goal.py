from uuid import UUID

from studytracker.domain.errors.base import app_error


@app_error
class InvalidPeriodRange:
    message: str = "Start period should be less than the end period"


@app_error
class GoalNotFound:
    message: str = "Goal not found"
    goal_id: UUID
