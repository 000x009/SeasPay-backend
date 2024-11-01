from src.application.common.dal.user_commission import UserCommissionDAL
from src.application.common.uow import UoW
from src.application.dto.user_commission import (
    UserCommissionDTO,
    GetUserCommissionDTO,
    CreateUserCommissionDTO,
    UpdateUserCommissionDTO,
)
from src.domain.entity.user_commission import UserCommission
from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_commission import (
    UserWithdrawCommission,
    UserTransferCommission,
    UserDigitalProductCommission,
)
from src.domain.exceptions.user_commission import UserCommissionNotFoundError


class UserCommissionService:
    def __init__(
        self,
        dal: UserCommissionDAL,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.uow = uow

    async def add(self, data: CreateUserCommissionDTO) -> UserCommissionDTO:
        user_commission = await self.dal.insert(UserCommission(
            user_id=UserID(data.user_id),
            transfer=UserTransferCommission(data.transfer),
            withdraw=UserWithdrawCommission(data.withdraw),
            digital_product=UserDigitalProductCommission(data.digital_product),
        ))
        await self.uow.commit()

        return UserCommissionDTO(
            user_id=user_commission.user_id.value,
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        )

    async def get(self, data: GetUserCommissionDTO) -> UserCommissionDTO:
        user_commission = await self.dal.get(UserID(data.user_id))
        if not user_commission:
            raise UserCommissionNotFoundError(f"Commission not found for user: <{data.user_id}>")

        return UserCommissionDTO(
            user_id=user_commission.user_id.value,
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        )

    async def update(self, data: UpdateUserCommissionDTO) -> UserCommissionDTO:
        user_commission = await self.dal.update(UserCommission(
            user_id=UserID(data.user_id),
            transfer=UserTransferCommission(data.transfer),
            withdraw=UserWithdrawCommission(data.withdraw),
            digital_product=UserDigitalProductCommission(data.digital_product),
        ))

        return UserCommissionDTO(
            user_id=user_commission.user_id.value,
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        )
