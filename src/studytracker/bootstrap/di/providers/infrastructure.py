from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from studytracker.infrastructure.database.config import DatabaseConfig


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(config.uri)
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
