from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from studytracker.api import add_exception_handler, add_routers
from studytracker.bootstrap.config import Config, get_config_path, load_config
from studytracker.bootstrap.di.container import get_async_contatiner


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    dishka_container = get_async_contatiner(config)
    setup_dishka(dishka_container, app)

    add_routers(app)
    add_exception_handler(app)

    return app


def get_fastapi_app() -> FastAPI:
    config = load_config(get_config_path())
    app = create_app(config)

    return app
