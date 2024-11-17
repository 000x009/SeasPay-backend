from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.user_topic import TopicNotFoundError


async def topic_not_found_handler(request: Request, exc: TopicNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )
