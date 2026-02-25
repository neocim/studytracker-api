from typing import override
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from studytracker.domain.entities.goal import Goal
from studytracker.domain.readers.goal import GoalReader
from studytracker.infrastructure.database.models.goal import GOALS_TABLE


class SQLAlchemyGoalReader(GoalReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def get_by_id(self, goal_id: UUID, user_id: UUID) -> Goal | None:
        query = select(Goal).where(GOALS_TABLE.c.user_id == user_id).where(GOALS_TABLE.c.id == goal_id)
        result = (await self._session.execute(query)).scalar_one_or_none()

        return result

    @override
    async def get_with_subgoals(self, goal_id: UUID, user_id: UUID) -> Goal | None:
        query = (
            select(Goal)
            .where(GOALS_TABLE.c.user_id == user_id)
            .where(GOALS_TABLE.c.id == goal_id)
            .options(selectinload(Goal._subgoals))  # noqa: SLF001
        )
        result: Goal = (await self._session.execute(query)).scalar_one_or_none()

        return result

    @override
    async def exists(self, goal_id: UUID) -> bool:
        query = select(exists().where(GOALS_TABLE.c.id == goal_id))
        result: bool = (await self._session.execute(query)).scalar_one()

        return result
