import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.main.ioc import DALProvider, DatabaseProvider, ServiceProvider
from src.presentation import include_all_routers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


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
    container = make_async_container(DALProvider(), DatabaseProvider(), ServiceProvider())
    setup_dishka(container, app)

    logging.info('App successfully created.')

    return app


app = create_app()
