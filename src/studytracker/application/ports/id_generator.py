from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IDGenerator(Protocol):
    @abstractmethod
    def get_uuid(self) -> UUID:
        raise NotImplementedError
