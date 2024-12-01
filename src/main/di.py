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
    RequisiteDALImpl,
    CryptoRequisiteDALImpl,
    CardRequisiteDALImpl,
)
from src.application.common.dal.requisite import RequisiteDAL
from src.application.common.dal.crypto_requisite import CryptoRequisiteDAL
from src.application.common.dal.card_requisite import CardRequisiteDAL
from src.application.common.dal.platform_product import PlatformProductDAL
from src.infrastructure.dal.platform_product import PlatformProductDALImpl
from src.application.services.platform_product import PlatformProductService
from src.application.common.dal.platform import PlatformDAL
from src.infrastructure.dal.platform import PlatformDALImpl
from src.application.services.platform import PlatformService
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
from src.application.services.crypto_requisite import CryptoRequisiteService
from src.application.services.card_requisite import CardRequisiteService
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
from src.application.services.requisite import RequisiteService


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
    platform_dal = provide(PlatformDALImpl, scope=Scope.REQUEST, provides=PlatformDAL)
    user_commission_dal = provide(UserCommissionDALImpl, scope=Scope.REQUEST, provides=UserCommissionDAL)
    uow = provide(SAUoW, scope=Scope.REQUEST, provides=UoW)
    platform_product_dal = provide(PlatformProductDALImpl, scope=Scope.REQUEST, provides=PlatformProductDAL)
    requisite_dal = provide(RequisiteDALImpl, scope=Scope.REQUEST, provides=RequisiteDAL)
    crypto_requisite_dal = provide(CryptoRequisiteDALImpl, scope=Scope.REQUEST, provides=CryptoRequisiteDAL)
    card_requisite_dal = provide(CardRequisiteDALImpl, scope=Scope.REQUEST, provides=CardRequisiteDAL)
    product_application_dal = provide(
        ProductApplicationDALImpl, scope=Scope.REQUEST, provides=ProductApplicationDALImpl
    )
    digital_product_details_dal = provide(
        DigitalProductDetailsDAL, scope=Scope.REQUEST, provides=DigitalProductDetailsDAL
    )


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
    platform_service = provide(PlatformService, scope=Scope.REQUEST, provides=PlatformService)
    user_commission_service = provide(UserCommissionService, scope=Scope.REQUEST, provides=UserCommissionService)
    platform_product_service = provide(PlatformProductService, scope=Scope.REQUEST, provides=PlatformProductService)
    requisite_service = provide(RequisiteService, scope=Scope.REQUEST, provides=RequisiteService)
    crypto_requisite_service = provide(CryptoRequisiteService, scope=Scope.REQUEST, provides=CryptoRequisiteService)
    card_requisite_service = provide(CardRequisiteService, scope=Scope.REQUEST, provides=CardRequisiteService)
    product_application_service = provide(
        ProductApplicationService, scope=Scope.REQUEST, provides=ProductApplicationService
    )
    digital_product_details_service = provide(
        DigitalProductDetailsService, scope=Scope.REQUEST, provides=DigitalProductDetailsService
    )


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
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['POST', 'PUT', 'GET'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }]
        }

        s3_client.put_bucket_cors(
            Bucket=settings.cloud_settings.receipts_bucket_name,
            CORSConfiguration=cors_configuration
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
