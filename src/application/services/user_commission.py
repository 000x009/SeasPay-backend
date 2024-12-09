from decimal import Decimal

from src.application.common.dal.user_commission import UserCommissionDAL
from src.application.common.uow import UoW
from src.application.dto.user_commission import (
    UserCommissionDTO,
    GetUserCommissionDTO,
    CreateUserCommissionDTO,
    UpdateUserCommissionDTO,
    CountCommissionDTO,
    CountCommissionResultDTO,
)
from src.domain.entity.user_commission import UserCommission
from src.domain.value_objects.user import UserID
from src.domain.value_objects.user_commission import (
    UserWithdrawCommission,
    UserTransferCommission,
    UserDigitalProductCommission,
)
from src.domain.exceptions.user_commission import UserCommissionNotFoundError
from src.application.services.cryptopay import CryptopayService


class UserCommissionService:
    def __init__(
        self,
        dal: UserCommissionDAL,
        uow: UoW,
        cryptopay: CryptopayService,
    ) -> None:
        self.dal = dal
        self.uow = uow
        self.cryptopay = cryptopay

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
        await self.uow.commit()

        return UserCommissionDTO(
            user_id=user_commission.user_id.value,
            transfer=user_commission.transfer.value,
            withdraw=user_commission.withdraw.value,
            digital_product=user_commission.digital_product.value,
        )

    async def count_commission(self, data: CountCommissionDTO) -> CountCommissionResultDTO:
        user_commission = await self.dal.get(UserID(data.user_id))
        rate_usd_rub = await self.cryptopay.get_rub_usd_rate()
        amount_rub = Decimal(data.amount) * Decimal(rate_usd_rub.rate)
        if not user_commission:
            raise UserCommissionNotFoundError(f"Commission not found for user: <{data.user_id}>")

        withdraw_final_rub = user_commission.count_withdraw_commission(amount_rub)
        transfer_final_rub = user_commission.count_transfer_commission(amount_rub)
        digital_product_final_usd = user_commission.count_digital_product_commission(data.amount)

        digital_product_final_rub = round(digital_product_final_usd * Decimal(rate_usd_rub.rate), 1)
        withdraw_final_usd = user_commission.count_withdraw_commission(data.amount)
        transfer_final_usd = user_commission.count_transfer_commission(data.amount)

        return CountCommissionResultDTO(
            withdraw_final_rub=withdraw_final_rub,
            transfer_final_rub=transfer_final_rub,
            digital_product_final_rub=digital_product_final_rub,
            withdraw_final_usd=withdraw_final_usd,
            transfer_final_usd=transfer_final_usd,
            digital_product_final_usd=digital_product_final_usd,
        )
