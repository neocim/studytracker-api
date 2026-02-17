from uuid import UUID
from bazario import Sender
from dishka import FromDishka
from fastapi import APIRouter, Response, status
from dishka.integrations.fastapi import DishkaRoute


goals_router = APIRouter(route_class=DishkaRoute, prefix="/users/{user_id}")

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create(user_id: UUID, interactor: FromDishka[Sender]) -> Response:
    