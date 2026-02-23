import datetime
from datetime import date
from enum import StrEnum
from uuid import UUID

from studytracker.domain.entities.base import Entity
from studytracker.domain.errors.goal import InvalidPeriodRangeError


class GoalStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
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
        goal_status: GoalStatus = GoalStatus.PENDING,
        parent_id: UUID | None = None,
        description: str | None = None,
    ) -> None:
        super().__init__(entity_id=entity_id)

        self._validate_period_range()
        self._init_status()

        self._parent_id = parent_id
        self._user_id = user_id

        self._period_start = period_start
        self._period_end = period_end
        self._name = name
        self._description = description

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

    def _init_status(self) -> None:
        today = datetime.datetime.now(tz=datetime.UTC).date()

        if self._period_start > today:
            self._goal_status = GoalStatus.PENDING
        elif self._period_start <= today <= self._period_end:
            self._goal_status = GoalStatus.IN_PROGRESS
        elif self._period_end < today:
            self._goal_status = GoalStatus.COMPLETED

    def _validate_period_range(self) -> None:
        if self._period_start >= self._period_end:
            raise InvalidPeriodRangeError
