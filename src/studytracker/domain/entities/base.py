from collections.abc import Hashable
from typing import TypeVar, override

EntityID = TypeVar("EntityID")


class Entity[EntityID: Hashable]:
    def __init__(self, entity_id: EntityID) -> None:
        self._entity_id = entity_id

    @property
    def entity_id(self) -> EntityID:
        return self._entity_id

    @override
    def __hash__(self) -> int:
        return hash(self._entity_id)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return bool(self._entity_id == other._entity_id)
