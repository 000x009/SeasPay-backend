from typing import Optional, List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseUserDAL
from src.domain.entity.user import User
from src.domain.value_objects.user import UserID, JoinedAt, Commission, TotalWithdrawn
from src.infrastructure.data.models import UserModel


class UserDAL(BaseUserDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, user: User) -> User:
        user_model = UserModel(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            commission=user.commission.value,
            total_withdrawn=user.total_withdrawn.value
        )
        self._session.add(user_model)
        await self._session.flush(objects=[user_model])
        await self._session.commit()
        return user

    async def get_one(self, user_id: UserID) -> Optional[User]:
        query = select(UserModel).filter(UserModel.user_id == user_id.value)
        result = await self._session.execute(query)
        db_user = result.scalar()
        if not db_user:
            return None
        print(db_user.commission)
        return User(
            user_id=UserID(db_user.user_id),
            joined_at=JoinedAt(db_user.joined_at),
            commission=Commission(db_user.commission),
            total_withdrawn=TotalWithdrawn(db_user.total_withdrawn)
        )

    async def get_all_users(self) -> Optional[List[User]]:
        query = select(UserModel)
        result = await self._session.execute(query)
        db_users = result.scalars().all()

        if not db_users:
            return None
        
        return [
            User(
                user_id=UserID(db_user.user_id),
                joined_at=JoinedAt(db_user.joined_at),
                commission=Commission(db_user.commission),
                total_withdrawn=TotalWithdrawn(db_user.total_withdrawn)
            )
                for db_user in db_users
        ]

    async def update(self, user_id: UserID, user: User) -> None:
        query = update(UserModel).where(UserModel.user_id == user_id.value).values(
            commission=user.commission.value,
            total_withdrawn=user.total_withdrawn.value
        )
        await self._session.execute(query)
        await self._session.commit()
