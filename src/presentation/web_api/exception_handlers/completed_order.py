from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.completed_order import CompletedOrderNotFoundError, CompletedOrderDataError


async def completed_order_not_found_exception_handler(request: Request, exc: CompletedOrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


async def completed_order_data_exception_handler(request: Request, exc: CompletedOrderDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )
