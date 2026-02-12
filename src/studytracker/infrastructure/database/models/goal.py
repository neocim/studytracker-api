from sqlalchemy import UUID, Boolean, Column, Date, ForeignKey, String, Table

from studytracker.infrastructure.database.models.base import mapper_registry

goals_table = Table(
    "goals",
    mapper_registry.metadata,
    Column("id", UUID, index=True, primary_key=True, unique=True, nullable=False),
    Column("parent_id", UUID, ForeignKey("goals.id", ondelete="CASCADE"), nullable=True),
    Column("owner_id", UUID, index=True, nullable=False),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("is_success", Boolean, nullable=True),
    Column("period_start", Date, nullable=False),
    Column("period_end", Date, nullable=False),
)
