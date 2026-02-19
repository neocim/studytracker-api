from dishka import BaseScope, Provider, Scope, from_context

from studytracker.api.config import APIConfig
from studytracker.bootstrap.config import Config
from studytracker.infrastructure.database.config import DatabaseConfig


class ConfigProvider(Provider):
    scope: BaseScope | None = Scope.APP
    configs = from_context(Config) + from_context(APIConfig) + from_context(DatabaseConfig)
