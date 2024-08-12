from typing import Optional, List, TypeAlias

from sqlalchemy import insert, update, select, exists, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import DAL
from src.application.dto import UserDTO
from src.infrastructure.data.models import UserModel


_UserDBResult: TypeAlias = Result[tuple[UserModel]]


class UserDAL(DAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, **kwargs) -> None:
        query = insert(UserModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, user_id: int, **kwargs) -> None:
        query = update(UserModel).where(UserModel.user_id == user_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(UserModel, key) == value
                    for key, value in kwargs.items()
                    if hasattr(UserModel, key)
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def _get(self, **kwargs) -> Optional[_UserDBResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        query = select(UserModel).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs) -> Optional[UserDTO]:
        res = await self._get(**kwargs)

        if res:
            db_user = res.scalar_one_or_none()
            return UserDTO(
                user_id=db_user.user_id,
                joining_date=db_user.joining_date,
                email=db_user.email,
            )

    async def get_all(self, **kwargs) -> Optional[List[UserDTO]]:
        res = await self._get(**kwargs)

        if res:
            db_users = res.scalars().all()
            return [
                UserDTO(
                    user_id=db_user.user_id,
                    joining_date=db_user.joining_date,
                    email=db_user.email,
                )
                for db_user in db_users
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(UserModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
