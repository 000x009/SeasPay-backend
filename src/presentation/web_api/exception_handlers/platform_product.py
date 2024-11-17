from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.platform_product import PlatformProductDataError


async def platform_product_data_exception_handler(request: Request, exc: PlatformProductDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )
