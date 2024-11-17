from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.user import UserDataError, UserNotFoundError, NotAuthorizedError


async def user_data_exception_handler(request: Request, exc: UserDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


async def not_authorized_exception_handler(request: Request, exc: NotAuthorizedError):
    return JSONResponse(
        status_code=401,
        content={"message": exc.message}
    )
