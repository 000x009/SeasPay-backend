from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.platform import PlatformDataError


async def platform_data_exception_handler(request: Request, exc: PlatformDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )
