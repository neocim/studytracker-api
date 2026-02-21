from datetime import date
from uuid import UUID

from studytracker.domain.entities.base import Entity


class Goal(Entity[UUID]):
    def __init__(
        self,
        entity_id: UUID,
        user_id: UUID,
        period_start: date,
        period_end: date,
        name: str,
        parent_id: UUID | None = None,
        description: str | None = None,
        is_success: bool | None = None,
    ) -> None:
        super().__init__(entity_id=entity_id)

        self._parent_id = parent_id
        self._user_id = user_id
        self._period_start = period_start
        self._period_end = period_end
        self._name = name
        self._description = description
        self._is_success = is_success
