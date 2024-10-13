from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.uow import UoW


class SAUoW(UoW):
    """SQLAlchemy Unit of Work"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()
