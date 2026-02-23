import datetime
from datetime import date
from enum import StrEnum
from uuid import UUID

from studytracker.domain.entities.base import Entity
from studytracker.domain.errors.goal import (
    InvalidPeriodRangeError,
    InvalidStatusForCompletedGoalError,
    InvalidStatusForInProgressGoalError,
    InvalidStatusForNotStartedGoalError,
    InvalidSubgoalPeriodRangeError,
)


class GoalStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


VALID_STATUSES_FOR_COMPLETED_GOAL = [GoalStatus.SUCCEEDED, GoalStatus.FAILED, GoalStatus.CANCELED]
VALID_STATUSES_FOR_NOT_STARTED_GOAL = [GoalStatus.PENDING, GoalStatus.CANCELED]
VALID_STATUSES_FOR_IN_PROGRESS_GOAL = [GoalStatus.IN_PROGRESS, GoalStatus.CANCELED]


class Goal(Entity[UUID]):
    def __init__(
        self,
        entity_id: UUID,
        user_id: UUID,
        period_start: date,
        period_end: date,
        name: str,
        goal_status: GoalStatus | None = None,
        description: str | None = None,
    ) -> None:
        super().__init__(entity_id=entity_id)

        self._validate_period_range(period_start, period_end)
        self._goal_status = self._validate_and_get_status(period_start, period_end, goal_status)

        self._period_start = period_start
        self._period_end = period_end
        self._user_id = user_id
        self._name = name
        self._description = description

        self._parent: Goal | None = None
        self._subgoals: list[Goal] = []

    def set_name(self, new_name: str) -> None:
        self._name = new_name

    def set_description(self, new_description: str | None) -> None:
        self._description = new_description

    def add_subgoal(self, subgoal: "Goal") -> None:
        if subgoal.period_start < self._period_start or subgoal.period_end > self._period_end:
            raise InvalidSubgoalPeriodRangeError

        self._subgoals.append(subgoal)

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

        if period_start > today:
            return GoalStatus.PENDING
        if period_start <= today <= period_end:
            return GoalStatus.IN_PROGRESS
        return GoalStatus.FAILED

    def _validate_provided_status(
        self,
        period_start: date,
        period_end: date,
        goal_status: GoalStatus,
        today: date,
    ) -> None:
        if today > period_end and goal_status not in VALID_STATUSES_FOR_COMPLETED_GOAL:
            raise InvalidStatusForCompletedGoalError

        if period_start <= today <= period_end and goal_status not in VALID_STATUSES_FOR_IN_PROGRESS_GOAL:
            raise InvalidStatusForInProgressGoalError

        if period_start >= today and goal_status not in VALID_STATUSES_FOR_NOT_STARTED_GOAL:
            raise InvalidStatusForNotStartedGoalError

    def _validate_period_range(self, period_start: date, period_end: date) -> None:
        if period_start >= period_end:
            raise InvalidPeriodRangeError

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def parent(self) -> "Goal | None":
        return self._parent

    @property
    def parent_id(self) -> UUID | None:
        return self._parent.entity_id if self._parent else None

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
