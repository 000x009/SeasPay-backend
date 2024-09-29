from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.application.common.dal.withdraw_method_dal import BaseWithdrawMethodDAL
from src.domain.entity.withdraw_method import (
    WithdrawMethod,
    CardMethod,
    CryptoMethod,
    DBCardMethod,
    DBCryptoMethod,
)
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.common.db_identity import DBIdentity
from src.domain.value_objects.withdraw_method import MethodEnum, Method, CardNumber, CardHolderName, CryptoAddress, Network
from src.infrastructure.data.models import (
    WithdrawMethodModel,
    CardMethodModel,
    CryptoMethodModel,
)


class WithdrawMethodDAL(BaseWithdrawMethodDAL):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, withdraw_method: WithdrawMethod) -> None:
        if isinstance(withdraw_method, CardMethod):
            model = CardMethodModel(
                order_id=withdraw_method.order_id.value,
                method=MethodEnum.CARD.value,
                card_number=withdraw_method.card_number.value,
                card_holder_name=withdraw_method.card_holder_name.value
            )
        elif isinstance(withdraw_method, CryptoMethod):
            model = CryptoMethodModel(
                order_id=withdraw_method.order_id.value,
                method=MethodEnum.CRYPTO.value,
                crypto_address=withdraw_method.crypto_address.value,
                network=withdraw_method.network.value
            )

        self.session.add(model)
        await self.session.flush()
    
    async def get(self, order_id: OrderID) -> Optional[WithdrawMethod]:
        query = select(WithdrawMethodModel).where(WithdrawMethodModel.order_id == order_id.value)
        result = await self.session.execute(query)
        db_withdraw_method = result.scalar_one_or_none()

        if db_withdraw_method:
            if db_withdraw_method.method == MethodEnum.CARD.value:
                return DBCardMethod(
                    id=DBIdentity(db_withdraw_method.id),
                    order_id=OrderID(db_withdraw_method.order_id),
                    method=Method(MethodEnum.CARD),
                    card_number=CardNumber(db_withdraw_method.card_number),
                    card_holder_name=CardHolderName(db_withdraw_method.card_holder_name)
                )
            elif db_withdraw_method.method == MethodEnum.CRYPTO.value:
                return DBCryptoMethod(
                    id=DBIdentity(db_withdraw_method.id),
                    order_id=OrderID(db_withdraw_method.order_id),
                    method=Method(MethodEnum.CRYPTO),
                    crypto_address=CryptoAddress(db_withdraw_method.crypto_address),
                    network=Network(db_withdraw_method.network)
                )
        return None
