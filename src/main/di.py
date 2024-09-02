from typing import AsyncGenerator, List
from aiohttp import ClientSession
from dishka import Provider, provide, Scope, AsyncContainer, make_async_container

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.infrastructure.dal import UserDAL
from src.application.services.user import UserService
from src.infrastructure.config import load_settings


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


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)


def setup_providers() -> List[Provider]:
    return [
        DatabaseProvider(),
        DALProvider(),
        ServiceProvider(),
    ]


def get_di_container() -> AsyncContainer:
    providers = setup_providers()
    return make_async_container(*providers)
