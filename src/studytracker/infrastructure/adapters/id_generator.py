import uuid
from typing import override
from uuid import UUID

from studytracker.application.ports.id_generator import IDGenerator


class IDGeneratorImpl(IDGenerator):
    @override
    def get_uuid(self) -> UUID:
        return uuid.uuid4()
