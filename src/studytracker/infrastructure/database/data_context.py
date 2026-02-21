from sqlalchemy.ext.asyncio import AsyncSession

from studytracker.application.ports.data_context import DataContext
from studytracker.domain.repositories.goal_repository import GoalRepository


class SQLAlchemyDataContext(DataContext):
    goal_repository: GoalRepository

    def __init__(self, goal_repository: GoalRepository, session: AsyncSession) -> None:
        self._session = session
        self.goal_repository = goal_repository

    async def commit(self) -> None:
        await self._session.commit()
