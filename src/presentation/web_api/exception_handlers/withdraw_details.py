from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.withdraw_details import WithdrawDetailsDataError, WithdrawDetailsNotFound


async def withdraw_details_data_error_handler(request: Request, exc: WithdrawDetailsDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


async def withdraw_details_not_found_handler(request: Request, exc: WithdrawDetailsNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )
