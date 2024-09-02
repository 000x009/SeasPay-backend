import logging
from contextlib import asynccontextmanager

from aiogram import Bot

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from src.main.di import get_di_container
from src.presentation import include_all_routers
from src.infrastructure.config import load_bot_settings
from src.main.bot import get_dispatcher


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     config = load_bot_settings()
#     bot = Bot(token=config.bot_token)
#     dispatcher = get_dispatcher()
#     await bot.set_webhook(
#         config.webhook_url,
#         allowed_updates=dispatcher.resolve_used_update_types(),
#         drop_pending_updates=True,
#     )
#     yield
#     await bot.delete_webhook(drop_pending_updates=True)
#     await bot.close()


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
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

    logging.info('App successfully created.')

    return app


app = create_app()
