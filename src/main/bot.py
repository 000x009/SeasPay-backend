import logging
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dishka import Scope
from dishka.integrations.aiogram import setup_dishka

from aiogram_dialog import setup_dialogs

from aiogram_album.ttl_cache_middleware import TTLCacheAlbumMiddleware

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder

from src.infrastructure.config import load_bot_settings
from src.main.di import get_di_container
from src.presentation.telegram.handlers import all_handlers
from src.presentation.telegram.dialogs import dialogs
from src.presentation.telegram.middlewares import LoginMiddleware
from src.presentation.telegram.dialogs.common.message_manager import YandexStorageMedia


logger = logging.getLogger(__name__)


@asynccontextmanager
async def setup_bot_dishka(dispatcher: Dispatcher) -> AsyncGenerator[None, None]:
    container = get_di_container()
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    yield
    await container.close()


def get_dispatcher() -> Dispatcher:
    storage = RedisStorage.from_url(
        'redis://redis:6379/0',
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dispatcher = Dispatcher(storage=storage)
    dispatcher.include_routers(*all_handlers)
    dispatcher.include_routers(*dialogs)
    LoginMiddleware(dishka_container=get_di_container(), router=dispatcher)
    TTLCacheAlbumMiddleware(router=dispatcher)

    return dispatcher


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    dispatcher = get_dispatcher()
    config = load_bot_settings()
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    container = get_di_container()
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    setup_dialogs(dispatcher, message_manager=YandexStorageMedia(container))

    try:
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        await container.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
