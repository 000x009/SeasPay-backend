from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.purchase_request import PurchaseRequestAlreadyTaken, PurchaseRequestNotFound


async def request_not_found_handler(request: Request, exc: PurchaseRequestNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )


async def request_already_taken_handler(request: Request, exc: PurchaseRequestAlreadyTaken):
    return JSONResponse(
        status_code=401,
        content={"message": exc.message}
    )
