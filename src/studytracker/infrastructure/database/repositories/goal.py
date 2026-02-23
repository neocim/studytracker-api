from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from studytracker.domain.entities.goal import Goal
from studytracker.domain.repositories.goal import GoalRepository


class SQLAlchemyGoalRepository(GoalRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    def add(self, goal: Goal) -> None:
        self._session.add(goal)

    @override
    async def delete(self, goal: Goal) -> None:
        return await self._session.delete(goal)
