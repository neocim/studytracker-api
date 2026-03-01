import datetime
from datetime import date
from enum import StrEnum
from uuid import UUID

from studytracker.domain.entities.base import Entity
from studytracker.domain.errors.goal import (
    InvalidPeriodRangeError,
    InvalidStatusForActiveGoalError,
    InvalidStatusForCompletedGoalError,
    InvalidStatusForNotStartedGoalError,
    InvalidSubgoalPeriodRangeError,
)


class GoalStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


VALID_STATUSES_FOR_SUCCEEDED_GOAL = [GoalStatus.SUCCEEDED, GoalStatus.FAILED, GoalStatus.CANCELLED]
VALID_STATUSES_FOR_NOT_STARTED_GOAL = [GoalStatus.PENDING, GoalStatus.CANCELLED]
VALID_STATUSES_FOR_ACTIVE_GOAL = [GoalStatus.ACTIVE, GoalStatus.CANCELLED]


class Goal(Entity[UUID]):
    def __init__(
        self,
        entity_id: UUID,
        user_id: UUID,
        period_start: date,
        period_end: date,
        name: str,
        parent: "Goal" | None = None,
        description: str | None = None,
        goal_status: GoalStatus | None = None,
    ) -> None:
        super().__init__(entity_id=entity_id)

        self._validate_period_range(period_start, period_end)
        self._goal_status = self._validate_and_get_status(period_start, period_end, goal_status)

        self._user_id = user_id
        self._period_start = period_start
        self._period_end = period_end
        self._name = name
        self._description = description

        self._parent = parent
        self._parent_id = parent.entity_id if parent is not None else None
        self._subgoals: list[Goal] = []

    def set_name(self, new_name: str) -> None:
        self._name = new_name

    def set_description(self, new_description: str | None) -> None:
        self._description = new_description

    def set_status(self, goal_status: GoalStatus) -> None:
        if self._goal_status == goal_status:
            return

        today = self._get_today()
        self._validate_status(self._period_start, self._period_end, today, goal_status)
        self._goal_status = goal_status

    def set_periods(
        self,
        new_start: date | None,
        new_end: date | None,
    ) -> None:
        if new_start is None and new_end is None:
            return
        period_start = new_start if new_start is not None else self._period_start
        period_end = new_end if new_end is not None else self._period_end

        self._validate_period_range(period_start, period_end)
        if self._parent is not None:
            self._validate_subgoal_periods(
                parent=self._parent,
                period_start=period_start,
                period_end=period_end,
            )
        self._period_start = period_start
        self._period_end = period_end

        self._goal_status = self._validate_and_get_status(period_start, period_end)

    def add_subgoal(self, subgoal: "Goal") -> None:
        self._validate_subgoal_periods(
            parent=self,
            period_start=subgoal.period_start,
            period_end=subgoal.period_end,
        )
        self._subgoals.append(subgoal)

    def _validate_subgoal_periods(self, parent: "Goal", period_start: date, period_end: date) -> None:
        if period_start < parent.period_start or period_end > parent.period_end:
            raise InvalidSubgoalPeriodRangeError

    def _validate_and_get_status(
        self,
        period_start: date,
        period_end: date,
        goal_status: GoalStatus | None = None,
    ) -> GoalStatus:
        today = self._get_today()

        if goal_status is not None:
            self._validate_status(period_start, period_end, today, goal_status)
            return goal_status

        if period_start > today:
            return GoalStatus.PENDING
        if period_start <= today <= period_end:
            return GoalStatus.ACTIVE
        return GoalStatus.FAILED

    def _validate_status(
        self,
        period_start: date,
        period_end: date,
        today: date,
        goal_status: GoalStatus,
    ) -> None:
        self._validate_not_started_status(period_start, today, goal_status)
        self._validate_active_status(period_start, period_end, today, goal_status)
        self._validate_completed_status(period_end, today, goal_status)

    def _validate_not_started_status(
        self,
        period_start: date,
        today: date,
        goal_status: GoalStatus,
    ) -> None:
        if period_start > today and goal_status not in VALID_STATUSES_FOR_NOT_STARTED_GOAL:
            raise InvalidStatusForNotStartedGoalError

    def _validate_active_status(
        self,
        period_start: date,
        period_end: date,
        today: date,
        goal_status: GoalStatus,
    ) -> None:
        if period_start <= today <= period_end and goal_status not in VALID_STATUSES_FOR_ACTIVE_GOAL:
            raise InvalidStatusForActiveGoalError

    def _validate_completed_status(
        self,
        period_end: date,
        today: date,
        goal_status: GoalStatus,
    ) -> None:
        if today > period_end and goal_status not in VALID_STATUSES_FOR_SUCCEEDED_GOAL:
            raise InvalidStatusForCompletedGoalError

    def _validate_period_range(self, period_start: date, period_end: date) -> None:
        if period_start >= period_end:
            raise InvalidPeriodRangeError

    def _get_today(self) -> date:
        return datetime.datetime.now(tz=datetime.UTC).date()

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def parent_id(self) -> UUID | None:
        return self._parent_id

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

    @property
    def subgoals(self) -> list["Goal"]:
        return self._subgoals
