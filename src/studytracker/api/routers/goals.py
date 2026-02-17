from uuid import UUID

from bazario import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Response, status
from fastapi.routing import router

from studytracker.application.commands.create_goal import CreateGoalRequest

goals_router = APIRouter(route_class=DishkaRoute, prefix="/users/{user_id}")


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create(user_id: UUID, sender: FromDishka[Sender]) -> Response:
    response = sender.send(CreateGoalRequest())
