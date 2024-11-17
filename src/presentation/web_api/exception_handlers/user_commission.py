from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.user_commission import UserCommissionDataError, UserCommissionNotFoundError


async def commission_not_found_handler(request: Request, exc: UserCommissionNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


async def commission_data_error(request: Request, exc: UserCommissionDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )
