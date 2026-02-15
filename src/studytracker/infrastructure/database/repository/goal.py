from sqlalchemy.ext.asyncio import AsyncSession

from studytracker.domain.entity.goal import Goal
from studytracker.domain.repository.goal_repository import GoalRepository


class SQLAlchemyGoalRepository(GoalRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, goal: Goal) -> None:
        self._session.add(goal)

    async def delete(self, goal: Goal) -> None:
        return await self._session.delete(goal)