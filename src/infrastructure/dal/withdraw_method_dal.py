from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.application.common.dal.withdraw_method_dal import BaseWithdrawMethodDAL
from src.domain.entity.withdraw_method import WithdrawMethod, DBWithdrawMethod
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.withdraw_method import (
    MethodEnum,
    Method,
    CardNumber,
    CardHolderName,
    CryptoAddress,
    CryptoNetwork,
    WithdrawMethodID
)
from src.infrastructure.data.models import WithdrawMethodModel


class WithdrawMethodDAL(BaseWithdrawMethodDAL):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, withdraw_method: WithdrawMethod) -> DBWithdrawMethod:
        model = WithdrawMethodModel(
            order_id=withdraw_method.order_id.value,
            method=withdraw_method.method.value,
            card_number=withdraw_method.card_number.value,
            card_holder_name=withdraw_method.card_holder_name.value,
            crypto_address=withdraw_method.crypto_address.value,
            crypto_network=withdraw_method.crypto_network.value,
        )
        self.session.add(model)
        await self.session.flush()

        return DBWithdrawMethod(
            id=WithdrawMethodID(model.id),
            order_id=OrderID(model.order_id),
            method=Method(MethodEnum(model.method)),
            card_number=CardNumber(model.card_number),
            card_holder_name=CardHolderName(model.card_holder_name),
            crypto_address=CryptoAddress(model.crypto_address),
            crypto_network=CryptoNetwork(model.crypto_network),
        )

    async def get(self, order_id: OrderID) -> Optional[DBWithdrawMethod]:
        query = select(WithdrawMethodModel).filter_by(order_id=order_id.value)
        result = await self.session.execute(query)
        db_withdraw_method = result.scalar_one_or_none()
        if db_withdraw_method is None:
            return None

        return DBWithdrawMethod(
            id=WithdrawMethodID(db_withdraw_method.id),
            order_id=OrderID(db_withdraw_method.order_id),
            method=Method(db_withdraw_method.method),
            card_number=CardNumber(db_withdraw_method.card_number),
            card_holder_name=CardHolderName(db_withdraw_method.card_holder_name),
            crypto_address=CryptoAddress(db_withdraw_method.crypto_address),
            crypto_network=CryptoNetwork(db_withdraw_method.crypto_network),
        )
