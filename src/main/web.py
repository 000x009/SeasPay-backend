import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_redis_cache import FastApiRedisCache

from dishka.integrations.fastapi import setup_dishka

from src.main.di import get_di_container
from src.presentation import include_all_routers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     redis_cache = FastApiRedisCache()
#     redis_cache.init(
#         host_url="redis://localhost:6379",
#         prefix="myapi-cache",
#         response_header="X-MyAPI-Cache",
#         ignore_arg_types=[Request, Response]
#     )
#     # redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=True)
#     # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield


def create_app() -> FastAPI:
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_all_routers(app)
    setup_dishka(get_di_container(), app)

    return app


app = create_app()
