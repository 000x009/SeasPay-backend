from typing import Optional, Union

from src.infrastructure.dal.withdraw_method_dal import WithdrawMethodDAL
from src.application.dto.withdraw_method import AddCardMethodDTO, AddCryptoMethodDTO, CardMethodDTO, CryptoMethodDTO
from src.domain.entity.withdraw_method import CardMethod, CryptoMethod
from src.domain.value_objects.withdraw_method import MethodEnum, Method, CardNumber, CardHolderName, CryptoAddress, Network
from src.domain.value_objects.order import OrderID
from src.domain.exceptions.withdraw_method import WithdrawMethodNotFound


class WithdrawService:
    def __init__(self, dal: WithdrawMethodDAL):
        self.dal = dal

    async def add_card_method(self, data: AddCardMethodDTO) -> CardMethodDTO:
        await self.dal.insert(CardMethod(
            method=Method(MethodEnum.CARD),
            order_id=OrderID(data.order_id),
            card_number=CardNumber(data.card_number),
            card_holder_name=CardHolderName(data.card_holder_name),
        ))
    
    async def add_crypto_method(self, data: AddCryptoMethodDTO) -> CryptoMethodDTO:
        await self.dal.insert(CryptoMethod(
            method=Method(MethodEnum.CRYPTO),
            order_id=OrderID(data.order_id),
            crypto_address=CryptoAddress(data.crypto_address),
            network=Network(data.network),
        ))

    async def get_withdraw_method(self, order_id: OrderID) -> Union[CardMethodDTO, CryptoMethodDTO]:
        method = await self.dal.get(OrderID(order_id))
        if method is None:
            raise WithdrawMethodNotFound(f"Withdraw method not found for order: {order_id}")
        
        if method.method == MethodEnum.CARD:
            return CardMethodDTO(
                id=method.id,
                order_id=method.order_id,
                method=method.method,
                card_number=method.card_number,
                card_holder_name=method.card_holder_name,
            )
        elif method.method == MethodEnum.CRYPTO:
            return CryptoMethodDTO(
                id=method.id,
                order_id=method.order_id,
                method=method.method,
                crypto_address=method.crypto_address,
                network=method.network,
            )
