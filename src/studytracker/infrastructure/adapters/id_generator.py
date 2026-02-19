import uuid
from uuid import UUID

from studytracker.application.ports.id_generator import IDGenerator


class IDGeneratorImpl(IDGenerator):
    def get_uuid(self) -> UUID:
        return uuid.uuid4()
