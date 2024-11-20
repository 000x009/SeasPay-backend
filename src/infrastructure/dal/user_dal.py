from typing import Optional, List
from datetime import timedelta

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseUserDAL
from src.domain.entity.user import User
from src.domain.value_objects.user import UserID, JoinedAt, TotalWithdrawn, ReferralID
from src.infrastructure.data.models import UserModel
from src.domain.value_objects.statistics import TimeSpan


class UserDAL(BaseUserDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, user: User) -> User:
        user_model = UserModel(
            user_id=user.user_id.value,
            joined_at=user.joined_at.value,
            total_withdrawn=user.total_withdrawn.value,
            referral_id=user.referral_id.value if user.referral_id else None,
        )
        self._session.add(user_model)
        await self._session.flush(objects=[user_model])
        return user

    async def get_one(self, user_id: UserID) -> Optional[User]:
        query = select(UserModel).filter(UserModel.user_id == user_id.value)
        result = await self._session.execute(query)
        db_user = result.scalar()
        if not db_user:
            return None

        return User(
            user_id=UserID(db_user.user_id),
            joined_at=JoinedAt(db_user.joined_at),
            total_withdrawn=TotalWithdrawn(db_user.total_withdrawn),
            referral_id=ReferralID(db_user.referral_id) if db_user.referral_id else None,
        )

    async def get_all_users(self) -> Optional[List[User]]:
        query = select(UserModel)
        result = await self._session.execute(query)
        db_users = result.unique().scalars().all()
        if not db_users:
            return None

        return [
            User(
                user_id=UserID(db_user.user_id),
                joined_at=JoinedAt(db_user.joined_at),
                total_withdrawn=TotalWithdrawn(db_user.total_withdrawn),
                referral_id=ReferralID(db_user.referral_id) if db_user.referral_id else None,
            )
            for db_user in db_users
        ]

    async def update(self, user_id: UserID, user: User) -> None:
        query = update(UserModel).where(UserModel.user_id == user_id.value).values(
            total_withdrawn=user.total_withdrawn.value
        )
        await self._session.execute(query)

    async def get_new_users_amount(self, timespan: Optional[TimeSpan] = None) -> int:
        if timespan is not None:
            query = (
                select(func.count()).select_from(UserModel)
                .filter(UserModel.joined_at > func.now() - timedelta(days=timespan.value))
            )
        else:
            query = select(func.count()).select_from(UserModel)
        result = await self._session.execute(query)

        return result.scalar_one_or_none() or 0
