from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.application.common.dal.withdraw_details import BaseWithdrawDetailsDAL
from src.domain.entity.withdraw_details import WithdrawDetails
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.requisite import RequisiteId
from src.domain.value_objects.withdraw_method import WithdrawCommission, PaymentReceipt
from src.infrastructure.data.models import WithdrawDetailsModel


class WithdrawDetailsDAL(BaseWithdrawDetailsDAL):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, withdraw_method: WithdrawDetails) -> WithdrawDetails:
        model = WithdrawDetailsModel(
            order_id=withdraw_method.order_id.value,
            requisite_id=withdraw_method.requisite_id.value,
            payment_receipt=withdraw_method.payment_receipt.value,
            commission=withdraw_method.commission.value,
        )
        self.session.add(model)

        return WithdrawDetails(
            order_id=OrderID(model.order_id),
            requisite_id=RequisiteId(model.requisite_id),
            payment_receipt=PaymentReceipt(model.payment_receipt),
            commission=WithdrawCommission(model.commission),
        )

    async def get(self, order_id: OrderID) -> Optional[WithdrawDetails]:
        query = select(WithdrawDetailsModel).filter_by(order_id=order_id.value)
        result = await self.session.execute(query)
        db_withdraw_method = result.scalar_one_or_none()
        if db_withdraw_method is None:
            return None

        return WithdrawDetails(
            order_id=OrderID(db_withdraw_method.order_id),
            requisite_id=RequisiteId(db_withdraw_method.requisite_id),
            payment_receipt=PaymentReceipt(db_withdraw_method.payment_receipt),
            commission=WithdrawCommission(db_withdraw_method.commission),
        )
