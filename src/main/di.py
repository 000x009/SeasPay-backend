from typing import AsyncGenerator, List, AsyncIterable
from contextlib import asynccontextmanager

from dishka import Provider, provide, Scope, AsyncContainer, make_async_container

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.infrastructure.dal import (
    UserDAL,
    OrderDAL,
    FeedbackDAL,
    UserTopicDAL,
    CompletedOrderDAL,
    WithdrawMethodDAL,
)
from src.application.services.user import UserService
from src.application.services.order import OrderService
from src.application.services.feedback import FeedbackService
from src.application.services.user_topic import UserTopicService
from src.application.services.completed_order import CompletedOrderService
from src.application.services.withdraw_service import WithdrawService
from src.infrastructure.config import load_settings, load_bot_settings, BotSettings
from src.infrastructure.telegram import TelegramClient
from src.application.services.telegram_service import TelegramService
from src.application.common.telegram import TelegramClientInterface


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP, provides=AsyncEngine)
    async def get_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        settings = load_settings()
        engine = create_async_engine(url=settings.db.connection_url, pool_pre_ping=True)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session


class DALProvider(Provider):
    user_dal = provide(UserDAL, scope=Scope.REQUEST, provides=UserDAL)
    order_dal = provide(OrderDAL, scope=Scope.REQUEST, provides=OrderDAL)
    feedback_dal = provide(FeedbackDAL, scope=Scope.REQUEST, provides=FeedbackDAL)
    user_topic_dal = provide(UserTopicDAL, scope=Scope.REQUEST, provides=UserTopicDAL)
    completed_order_dal = provide(CompletedOrderDAL, scope=Scope.REQUEST, provides=CompletedOrderDAL)
    withdraw_method_dal = provide(WithdrawMethodDAL, scope=Scope.REQUEST, provides=WithdrawMethodDAL)


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)
    order_service = provide(OrderService, scope=Scope.REQUEST, provides=OrderService)
    feedback_service = provide(FeedbackService, scope=Scope.REQUEST, provides=FeedbackService)
    user_topic_service = provide(UserTopicService, scope=Scope.REQUEST, provides=UserTopicService)
    completed_order_service = provide(CompletedOrderService, scope=Scope.REQUEST, provides=CompletedOrderService)
    withdraw_service = provide(WithdrawService, scope=Scope.REQUEST, provides=WithdrawService)
    telegram_service = provide(TelegramService, scope=Scope.REQUEST, provides=TelegramService)

class TelegramProvider(Provider):
    @asynccontextmanager
    async def _get_bot(self, config: BotSettings) -> AsyncGenerator[Bot, None]:
        bot = Bot(
            token=config.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        yield bot
        await bot.session.close()

    @provide(scope=Scope.REQUEST, provides=TelegramClientInterface)
    async def get_telegram_client(self) -> AsyncGenerator[TelegramClientInterface, None]:
        config = load_bot_settings()
        async with self._get_bot(config) as bot:
            yield TelegramClient(bot=bot, config=config)


def setup_providers() -> List[Provider]:
    return [
        DatabaseProvider(),
        DALProvider(),
        ServiceProvider(),
        TelegramProvider(),
    ]


def get_di_container() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
