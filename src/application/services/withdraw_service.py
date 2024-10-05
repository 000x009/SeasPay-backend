from typing import Optional, Union

from src.infrastructure.dal.withdraw_method_dal import WithdrawMethodDAL
from src.application.dto.withdraw_method import AddWithdrawMethodDTO, GetWithdrawMethodDTO, WithdrawMethodDTO
from src.domain.value_objects.withdraw_method import (
    MethodEnum,
    Method,
    CardNumber,
    CardHolderName,
    CryptoAddress,
    CryptoNetwork,
    WithdrawMethodID,
)
from src.domain.entity.withdraw_method import WithdrawMethod
from src.domain.value_objects.order import OrderID
from src.domain.exceptions.withdraw_method import WithdrawMethodNotFound


class WithdrawService:
    def __init__(self, dal: WithdrawMethodDAL):
        self.dal = dal

    async def add_method(self, data: AddWithdrawMethodDTO) -> WithdrawMethodDTO:
        method = WithdrawMethod(
            order_id=OrderID(data.order_id),
            method=Method(data.method),
            card_number=CardNumber(data.card_number),
            card_holder_name=CardHolderName(data.card_holder_name),
            crypto_address=CryptoAddress(data.crypto_address),
            crypto_network=CryptoNetwork(data.network),
        )
        await self.dal.insert(method)

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
            network=method.crypto_network.value,
        )
