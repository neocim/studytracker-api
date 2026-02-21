from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from studytracker.application.ports.data_context import DataContext
from studytracker.domain.repositories.goal import GoalRepository


class SQLAlchemyDataContext(DataContext):
    def __init__(self, goal_repository: GoalRepository, session: AsyncSession) -> None:
        self._session = session
        self._goal_repository = goal_repository

    @override
    @property
    def goal_repository(self) -> GoalRepository:
        return self._goal_repository

    @override
    async def commit(self) -> None:
        await self._session.commit()
