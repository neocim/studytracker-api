from dishka import AsyncContainer, make_async_container

from studytracker.api.config import APIConfig
from studytracker.bootstrap.config import Config
from studytracker.bootstrap.di.providers.config import ConfigProvider
from studytracker.bootstrap.di.providers.infrastructure import InfrastructureProvider
from studytracker.infrastructure.database.config import DatabaseConfig


def get_async_contatiner(config: Config) -> AsyncContainer:
    providers = [
        ConfigProvider(),
        InfrastructureProvider(),
    ]
    context = {
        Config: config,
        APIConfig: config.api,
        DatabaseConfig: config.database,
    }

    container = make_async_container(*providers, context=context)
    return container
