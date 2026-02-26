from collections.abc import AsyncIterator

from dishka import Provider, Scope, WithParents, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from studytracker.infrastructure.adapters.goal_mapper import GoalMapperImpl
from studytracker.infrastructure.adapters.id_generator import IDGeneratorImpl
from studytracker.infrastructure.database.config import DatabaseConfig
from studytracker.infrastructure.database.data_context import SQLAlchemyDataContext
from studytracker.infrastructure.database.readers.goal import SQLAlchemyGoalReader
from studytracker.infrastructure.database.repositories.goal import SQLAlchemyGoalRepository


class InfrastructureProvider(Provider):
    id_generator = provide(WithParents[IDGeneratorImpl], scope=Scope.APP)
    goal_mapper = provide(WithParents[GoalMapperImpl], scope=Scope.APP)
    data_context = provide(WithParents[SQLAlchemyDataContext], scope=Scope.REQUEST)

    repositories = provide_all(WithParents[SQLAlchemyGoalRepository], scope=Scope.REQUEST)
    readers = provide_all(WithParents[SQLAlchemyGoalReader], scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    async def get_engine(self, config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(config.connection_url)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

        return factory

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session
