from typing import Optional, List
from dataclasses import asdict

from sqlalchemy import insert, update, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseUserDAL
from src.application.dto.user import UserDTO, CreateUserDTO, GetUserDTO
from src.infrastructure.data.models import UserModel
from src.domain.value_objects.user.user_id import UserID
from src.domain.entity.user import User


class UserDAL(BaseUserDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, values: CreateUserDTO) -> None:
        query = insert(UserModel).values(**asdict(values))
        await self._session.execute(query)
        await self._session.commit()

    async def exists(self, values: GetUserDTO) -> bool:
        query = select(
            exists().where(
                *(
                    getattr(UserModel, key) == value
                    for key, value in asdict(values).items()
                    if hasattr(UserModel, key)
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_one(self, values: GetUserDTO) -> Optional[UserDTO]:
        exists = await self.exists(**asdict(values))
        if not exists:
            return None
        
        query = select(UserModel).filter_by(**asdict(values))
        result = await self._session.execute(query)

        if result:
            db_user = result.scalar_one()
            return UserDTO(
                user_id=db_user.user_id,
                joined_at=db_user.joined_at,
                commission=db_user.commission,
                total_withdrawn=db_user.total_withdrawn,
            )

    async def get_all(self, values: GetUserDTO) -> Optional[List[UserDTO]]:
        exists = await self.exists(**asdict(values))
        if not exists:
            return None
        
        query = select(UserModel).filter_by(**asdict(values))
        result = await self._session.execute(query)

        if result:
            db_users = result.scalars().all()
            return [
                UserDTO(
                    user_id=db_user.user_id,
                    joined_at=db_user.joined_at,
                    commission=db_user.commission,
                    total_withdrawn=db_user.total_withdrawn,
                )
                for db_user in db_users
            ]

    # async def update(self, id_: UserID, values: User) -> None:
    #     query = update(UserModel).where(UserModel.user_id == id_.value).values(
    #         values.
    #     )
    #     await self._session.execute(query)
    #     await self._session.commit()
