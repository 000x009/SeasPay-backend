from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.user_commission import UserCommissionDAL
from src.domain.entity.user_commission import UserCommission
from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_commission import (
    UserTransferCommission,
    UserWithdrawCommission,
    UserDigitalProductCommission,
)
from src.infrastructure.data.models import UserCommissionModel


class UserCommissionDALImpl(UserCommissionDAL):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: UserID) -> Optional[UserCommission]:
        query = select(UserCommissionModel).filter_by(user_id=user_id.value)
        result = await self.session.execute(query)
        user_commission = result.scalar_one_or_none()

        return UserCommission(
            user_id=UserID(user_commission.user_id),
            transfer=UserTransferCommission(user_commission.transfer),
            withdraw=UserWithdrawCommission(user_commission.withdraw),
            digital_product=UserDigitalProductCommission(user_commission.digital_product),
        )

    async def update(self, user_commission: UserCommission) -> UserCommission:
        query = update(UserCommissionModel).values(
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        )
        await self.session.execute(query)

        return user_commission

    async def insert(self, user_commission: UserCommission) -> UserCommission:
        user_commission = UserCommissionModel(
            user_id=user_commission.user_id.value,
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        )
        self.session.add(user_commission)

        return UserCommission(
            user_id=UserID(user_commission.user_id),
            transfer=UserTransferCommission(user_commission.transfer),
            withdraw=UserWithdrawCommission(user_commission.withdraw),
            digital_product=UserDigitalProductCommission(user_commission.digital_product),
        )
