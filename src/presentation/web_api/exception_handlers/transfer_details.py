from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.transfer_details import TransferDetailsDataError, TransferDetailsNotFound


async def transfer_not_found_handler(request: Request, exc: TransferDetailsNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


async def transfer_data_handler(request: Request, exc: TransferDetailsDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )
