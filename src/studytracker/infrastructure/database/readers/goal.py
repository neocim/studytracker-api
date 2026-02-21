from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from studytracker.domain.entities.goal import Goal
from studytracker.domain.readers.goal import GoalReader
from studytracker.infrastructure.database.models.goal import GOALS_TABLE


class SQLAlchemyGoalReader(GoalReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        return await self._session.get(Goal, goal_id)

    async def exists(self, goal_id: UUID) -> bool:
        query = select(exists().where(GOALS_TABLE.c.id == goal_id))

        result = await self._session.execute(query)
        return result.scalar_one()
