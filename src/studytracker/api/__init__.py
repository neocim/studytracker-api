from fastapi import FastAPI

from studytracker.api.error_handler import app_error_handler
from studytracker.api.routers.goals import router as goals_router


def add_routers(app: FastAPI) -> None:
    app.include_router(goals_router)


def add_exception_handler(app: FastAPI) -> None:
    app.add_exception_handler(Exception, app_error_handler)


__all__ = [
    "add_exception_handler",
    "add_routers",
]
