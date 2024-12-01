from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.requisite import RequisiteNotFound


async def requisite_not_found_handler(request: Request, exc: RequisiteNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )
