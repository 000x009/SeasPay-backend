import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_redis_cache import FastApiRedisCache

from dishka.integrations.fastapi import setup_dishka

from src.main.di import get_di_container
from src.presentation import include_all_routers, include_exception_handlers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_all_routers(app)
    include_exception_handlers(app)
    setup_dishka(get_di_container(), app)

    return app


app = create_app()
