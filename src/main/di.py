from typing import AsyncGenerator, List
from aiohttp import BasicAuth
from contextlib import asynccontextmanager

from dishka import Provider, provide, Scope, AsyncContainer, make_async_container

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.infrastructure.dal import UserDAL, OrderDAL, FeedbackDAL, UserTopicDAL, CompletedOrderDAL
from src.application.services.user import UserService
from src.application.services.order import OrderService
from src.application.services.feedback import FeedbackService
from src.application.services.user_topic import UserTopicService
from src.application.services.completed_order import CompletedOrderService
from src.infrastructure.config import load_settings, load_bot_settings, BotSettings
from src.infrastructure.telegram import TelegramTopicManager
from src.application.services.telegram_order_sender import TelegramOrderSender


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP, provides=AsyncEngine)
    def get_engine(self) -> AsyncEngine:
        settings = load_settings()
        return create_async_engine(url=settings.db.connection_url)

    @provide(scope=Scope.APP, provides=async_sessionmaker[AsyncSession])
    def get_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_async_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            yield session


class DALProvider(Provider):
    user_dal = provide(UserDAL, scope=Scope.REQUEST, provides=UserDAL)
    order_dal = provide(OrderDAL, scope=Scope.REQUEST, provides=OrderDAL)
    feedback_dal = provide(FeedbackDAL, scope=Scope.REQUEST, provides=FeedbackDAL)
    user_topic_dal = provide(UserTopicDAL, scope=Scope.REQUEST, provides=UserTopicDAL)
    completed_order_dal = provide(CompletedOrderDAL, scope=Scope.REQUEST, provides=CompletedOrderDAL)


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)
    order_service = provide(OrderService, scope=Scope.REQUEST, provides=OrderService)
    feedback_service = provide(FeedbackService, scope=Scope.REQUEST, provides=FeedbackService)
    user_topic_service = provide(UserTopicService, scope=Scope.REQUEST, provides=UserTopicService)
    completed_order_service = provide(CompletedOrderService, scope=Scope.REQUEST, provides=CompletedOrderService)


# class ConfigProvider(Provider):
#     config = provide(BotSettings, scope=Scope.ACTION, provides=BotSettings)


class TelegramProvider(Provider):
    telegram_order_sender = provide(TelegramOrderSender, scope=Scope.REQUEST, provides=TelegramOrderSender)

    @asynccontextmanager
    async def _get_bot(self, config: BotSettings) -> AsyncGenerator[Bot, None]:
        proxy_url = "http://95.215.1.84:58656"
        auth = BasicAuth("TyTdCBZZ", "c9RVSrf7")
        client_session = AiohttpSession(proxy=(proxy_url, auth))
        bot = Bot(
            token=config.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            session=client_session
        )
        yield bot
        await bot.session.close()
        await client_session.close()

    @provide(scope=Scope.REQUEST, provides=TelegramTopicManager)
    async def get_telegram_topic_manager(self) -> AsyncGenerator[TelegramTopicManager, None]:
        config = load_bot_settings()
        async with self._get_bot(config) as bot:
            yield TelegramTopicManager(
                bot=bot,
                config=config,
            )


def setup_providers() -> List[Provider]:
    return [
        DatabaseProvider(),
        DALProvider(),
        ServiceProvider(),
        TelegramProvider(),
        # ConfigProvider(),
    ]


def get_di_container() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
