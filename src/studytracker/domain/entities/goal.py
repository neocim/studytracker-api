import datetime
from datetime import date
from enum import StrEnum
from uuid import UUID

from studytracker.domain.entities.base import Entity
from studytracker.domain.errors.goal import (
    InvalidPeriodRangeError,
    InvalidStatusForCompletedGoalError,
    InvalidStatusForNotStartedGoalError,
)


class GoalStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class Goal(Entity[UUID]):
    def __init__(
        self,
        entity_id: UUID,
        user_id: UUID,
        period_start: date,
        period_end: date,
        name: str,
        goal_status: GoalStatus | None = None,
        parent_id: UUID | None = None,
        description: str | None = None,
    ) -> None:
        super().__init__(entity_id=entity_id)

        self._validate_period_range(period_start, period_end)
        self._goal_status = self._validate_and_get_status(period_start, period_end, goal_status)

        self._period_start = period_start
        self._period_end = period_end
        self._parent_id = parent_id
        self._user_id = user_id
        self._name = name
        self._description = description

    def _validate_and_get_status(
        self,
        period_start: date,
        period_end: date,
        goal_status: GoalStatus | None = None,
    ) -> GoalStatus:
        today = datetime.datetime.now(tz=datetime.UTC).date()

        if goal_status is not None:
            self._validate_provided_status(period_start, period_end, goal_status, today)
            return goal_status

        return (
            GoalStatus.PENDING
            if period_start > today
            else GoalStatus.IN_PROGRESS
            if period_start <= today <= period_end
            else GoalStatus.FAILED
        )

    def _validate_provided_status(
        self,
        period_start: date,
        period_end: date,
        goal_status: GoalStatus,
        today: date,
    ) -> None:
        if today > period_end and goal_status not in [
            GoalStatus.SUCCEEDED,
            GoalStatus.FAILED,
            GoalStatus.CANCELED,
        ]:
            raise InvalidStatusForCompletedGoalError

        if period_start > today and goal_status not in [GoalStatus.PENDING, GoalStatus.CANCELED]:
            raise InvalidStatusForNotStartedGoalError

    def _validate_period_range(self, period_start: date, period_end: date) -> None:
        if period_start >= period_end:
            raise InvalidPeriodRangeError

    @property
    def parent_id(self) -> UUID | None:
        return self._parent_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def period_start(self) -> date:
        return self._period_start

    @property
    def period_end(self) -> date:
        return self._period_end

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def goal_status(self) -> GoalStatus:
        return self._goal_status
