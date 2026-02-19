from fastapi import FastAPI


def add_routers(app: FastAPI) -> None:
    app.include_router(goals_router)
