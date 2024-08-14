from typing import Optional, List, TypeAlias
from dataclasses import asdict

from sqlalchemy import insert, update, select, exists, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common import BaseUserDAL
from src.application.dto import UserDTO, UpdateUserDTO
from src.infrastructure.data.models import UserModel
from src.domain.value_objects.user.user_id import UserID


_UserDBResult: TypeAlias = Result[tuple[UserModel]]


class UserDAL(BaseUserDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, values: UserDTO) -> None:
        query = insert(UserModel).values(**asdict(values))
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, user_id: UserID, values: UpdateUserDTO) -> None:
        query = update(UserModel).where(UserModel.user_id == user_id.value).values(**asdict(values))
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, values: UserDTO) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(UserModel, key) == value
                    for key, value in asdict(values).items()
                    if hasattr(UserModel, key)
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one()

    async def _get(self, values: UserDTO) -> Optional[_UserDBResult]:
        exists = await self.exists(values=values)
        if not exists:
            return None

        query = select(UserModel).filter_by(**asdict(UserDTO))
        result = await self.session.execute(query)
        return result

    async def get_one(self, values: UserDTO) -> Optional[UserDTO]:
        res = await self._get(values=values)

        if res:
            db_user = res.scalar_one_or_none()
            return UserDTO(
                user_id=db_user.user_id,
                joining_date=db_user.joining_date,
                email=db_user.email,
            )

    async def get_all(self, values: UserDTO) -> Optional[List[UserDTO]]:
        res = await self._get(**asdict(values))

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

    async def delete(self, values: UserDTO) -> None:
        query = delete(UserModel).filter_by(**asdict(values))
        await self.session.execute(query)
        await self.session.commit()
