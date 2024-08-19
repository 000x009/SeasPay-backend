import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.main.ioc import DALProvider, DatabaseProvider, ServiceProvider
from src.presentation.endpoints import user


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

container = make_async_container(DALProvider(), DatabaseProvider(), ServiceProvider())
setup_dishka(container, app)
