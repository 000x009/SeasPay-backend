from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.feedback import FeedbackDataError, FeedbackNotFoundError


async def feedback_data_exception_handler(request: Request, exc: FeedbackDataError):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message}
    )


async def feedback_not_found_exception_handler(request: Request, exc: FeedbackNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message}
    )
