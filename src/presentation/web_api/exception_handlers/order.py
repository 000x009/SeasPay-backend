from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.order import OrderAlreadyTakenError, OrderNotFoundError


async def order_not_found_exception_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


async def order_already_taken_exception_handler(request: Request, exc: OrderAlreadyTakenError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )
