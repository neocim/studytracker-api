from sqlalchemy import UUID, Column, Date, Enum, ForeignKey, String, Table

from studytracker.domain.entities.goal import Goal
from studytracker.infrastructure.database.models.base import MAPPER_REGISTRY

GOALS_TABLE = Table(
    "goals",
    MAPPER_REGISTRY.metadata,
    Column("id", UUID, index=True, primary_key=True, nullable=False),
    Column("parent_id", UUID, ForeignKey("goals.id", ondelete="CASCADE"), nullable=True),
    Column("user_id", UUID, index=True, nullable=False),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column(
        "goal_status",
        Enum("PENDING", "IN_PROGRESS", "SUCCEEDED", "FAILED", "CANCELED", name="goal_status_enum"),
        nullable=False,
    ),
    Column("period_start", Date, nullable=False),
    Column("period_end", Date, nullable=False),
)

MAPPER_REGISTRY.map_imperatively(
    Goal,
    GOALS_TABLE,
    properties={
        "_entity_id": GOALS_TABLE.c.id,
        "_parent_id": GOALS_TABLE.c.parent_id,
        "_user_id": GOALS_TABLE.c.user_id,
        "_period_start": GOALS_TABLE.c.period_start,
        "_period_end": GOALS_TABLE.c.period_end,
        "_name": GOALS_TABLE.c.name,
        "_description": GOALS_TABLE.c.description,
        "_goal_status": GOALS_TABLE.c.goal_status,
    },
)
