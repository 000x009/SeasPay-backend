from typing import AsyncGenerator, List, AsyncIterable
from contextlib import asynccontextmanager

import boto3

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
    WithdrawDetailsDAL,
    UserCommissionDALImpl,
)
from src.application.common.dal.user_commission import UserCommissionDAL
from src.application.services.user_commission import UserCommissionService
from src.application.services.user import UserService
from src.application.services.order import OrderService
from src.application.services.feedback import FeedbackService
from src.application.services.user_topic import UserTopicService
from src.application.services.completed_order import CompletedOrderService
from src.application.services.purchase_request import PurchaseRequestService
from src.infrastructure.dal.purchase_request import PurchaseRequestDalImpl
from src.application.services.withdraw_details import WithdrawService
from src.application.services.cloud import CloudService
from src.application.services.transfer_details import TransferDetailsService
from src.infrastructure.dal.tranfer_details import TransferDetailsDAL
from src.application.services.statistics import StatisticsService
from src.application.services.digital_product_details import DigitalProductDetailsService
from src.infrastructure.dal.digital_product_details import DigitalProductDetailsDAL
from src.infrastructure.config import load_settings, load_bot_settings, BotSettings
from src.infrastructure.telegram import TelegramClient
from src.application.services.telegram_service import TelegramService
from src.application.services.product_application import ProductApplicationService
from src.infrastructure.dal.product_application import ProductApplicationDALImpl
from src.application.common.telegram import TelegramClientInterface
from src.application.common.uow import UoW
from src.infrastructure.data.uow import SAUoW
from src.application.common.cloud_storage import CloudStorage
from src.infrastructure.cloud_storage import YandexCloudStorage


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
    withdraw_method_dal = provide(WithdrawDetailsDAL, scope=Scope.REQUEST, provides=WithdrawDetailsDAL)
    transfer_details_dal = provide(TransferDetailsDAL, scope=Scope.REQUEST, provides=TransferDetailsDAL)
    purchase_request_dal = provide(PurchaseRequestDalImpl, scope=Scope.REQUEST, provides=PurchaseRequestDalImpl)
    product_application_dal = provide(
        ProductApplicationDALImpl, scope=Scope.REQUEST, provides=ProductApplicationDALImpl
    )
    user_commission_dal = provide(UserCommissionDALImpl, scope=Scope.REQUEST, provides=UserCommissionDAL)
    digital_product_details_dal = provide(
        DigitalProductDetailsDAL, scope=Scope.REQUEST, provides=DigitalProductDetailsDAL
    )
    uow = provide(SAUoW, scope=Scope.REQUEST, provides=UoW)


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)
    order_service = provide(OrderService, scope=Scope.REQUEST, provides=OrderService)
    feedback_service = provide(FeedbackService, scope=Scope.REQUEST, provides=FeedbackService)
    user_topic_service = provide(UserTopicService, scope=Scope.REQUEST, provides=UserTopicService)
    completed_order_service = provide(CompletedOrderService, scope=Scope.REQUEST, provides=CompletedOrderService)
    withdraw_service = provide(WithdrawService, scope=Scope.REQUEST, provides=WithdrawService)
    telegram_service = provide(TelegramService, scope=Scope.REQUEST, provides=TelegramService)
    statistics_service = provide(StatisticsService, scope=Scope.REQUEST, provides=StatisticsService)
    transfer_details_service = provide(TransferDetailsService, scope=Scope.REQUEST, provides=TransferDetailsService)
    cloud_service = provide(CloudService, scope=Scope.REQUEST, provides=CloudService)
    purchase_request_service = provide(PurchaseRequestService, scope=Scope.REQUEST, provides=PurchaseRequestService)
    product_application_service = provide(
        ProductApplicationService, scope=Scope.REQUEST, provides=ProductApplicationService
    )
    digital_product_details_service = provide(
        DigitalProductDetailsService, scope=Scope.REQUEST, provides=DigitalProductDetailsService
    )
    user_commission_service = provide(UserCommissionService, scope=Scope.REQUEST, provides=UserCommissionService)


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


class APIClientProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=CloudStorage)
    async def get_yandex_cloud_client(self) -> YandexCloudStorage:
        settings = load_settings()
        session = boto3.session.Session()
        s3_client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=settings.cloud_settings.access_key_id,
            aws_secret_access_key=settings.cloud_settings.access_secret_key,
        )

        return YandexCloudStorage(client=s3_client)


def setup_providers() -> List[Provider]:
    return [
        DatabaseProvider(),
        DALProvider(),
        ServiceProvider(),
        TelegramProvider(),
        APIClientProvider(),
    ]


def get_di_container() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
