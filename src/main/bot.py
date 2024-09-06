import logging
import asyncio
from contextlib import asynccontextmanager

from dishka.integrations.aiogram import setup_dishka

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.infrastructure.config import load_bot_settings
from src.main.di import get_di_container


logger = logging.getLogger(__name__)


@asynccontextmanager
async def setup_bot_dishka(dispatcher: Dispatcher):
    container = get_di_container()
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    yield
    await container.close()


def get_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    setup_bot_dishka(dispatcher)

    return dispatcher


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    dispatcher = get_dispatcher()
    config = load_bot_settings()
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        await dispatcher.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
    