from src.infrastructure.dal.withdraw_method_dal import WithdrawMethodDAL
from src.application.dto.withdraw_method import AddWithdrawMethodDTO, GetWithdrawMethodDTO, WithdrawMethodDTO
from src.domain.value_objects.withdraw_method import (
    Method,
    CardNumber,
    CardHolderName,
    CryptoAddress,
    CryptoNetwork,
)
from src.domain.entity.withdraw_method import WithdrawMethod
from src.domain.value_objects.order import OrderID
from src.domain.exceptions.withdraw_method import WithdrawMethodNotFound
from src.application.common.uow import UoW


class WithdrawService:
    def __init__(
        self,
        dal: WithdrawMethodDAL,
        uow: UoW,
    ):
        self.dal = dal
        self.uow = uow

    async def add_method(self, data: AddWithdrawMethodDTO) -> WithdrawMethodDTO:
        method = WithdrawMethod(
            order_id=OrderID(data.order_id),
            method=Method(data.method),
            card_number=CardNumber(data.card_number),
            card_holder_name=CardHolderName(data.card_holder_name),
            crypto_address=CryptoAddress(data.crypto_address),
            crypto_network=CryptoNetwork(data.crypto_network),
        )
        withdraw_method = await self.dal.insert(method)
        await self.uow.flush()

        return WithdrawMethodDTO(
            id=withdraw_method.id.value,
            order_id=withdraw_method.order_id.value,
            method=withdraw_method.method.value,
            card_number=withdraw_method.card_number.value,
            card_holder_name=withdraw_method.card_holder_name.value,
            crypto_address=withdraw_method.crypto_address.value,
            crypto_network=withdraw_method.crypto_network.value,
        )

    async def get_withdraw_method(self, data: GetWithdrawMethodDTO) -> WithdrawMethodDTO:
        method = await self.dal.get(OrderID(data.order_id))
        if method is None:
            raise WithdrawMethodNotFound(f"Withdraw method not found for order: {data.order_id}")
        
        return WithdrawMethodDTO(
            id=method.id.value,
            order_id=method.order_id.value,
            method=method.method.value,
            card_number=method.card_number.value,
            card_holder_name=method.card_holder_name.value,
            crypto_address=method.crypto_address.value,
            crypto_network=method.crypto_network.value,
        )
