from fastapi import FastAPI

from studytracker.api.routers.goals import router as goals_router


def add_routers(app: FastAPI) -> None:
    app.include_router(goals_router)


def add_exception_handler(app: FastAPI) -> None:
    app.add_exception_handler(Exception, add_exception_handler)


__all__ = [
    "add_exception_handler",
    "add_routers",
]
