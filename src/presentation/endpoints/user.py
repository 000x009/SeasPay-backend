from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.services.user import UserService
from src.application.dto.user import CreateUserDTO


router = APIRouter(
    tags=['User'],
    route_class=DishkaRoute,
)


@router.post('/')
async def add_user(user_service: FromDishka[UserService]) -> JSONResponse:
    await user_service.add(CreateUserDTO(
        user_id=12823,
        email='email@gmail.com',
    ))

    return JSONResponse(content='success', status_code=200)
