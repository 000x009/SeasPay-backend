from typing import Optional

from sqlalchemy import insert,  select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseCompletedOrderDAL
from src.domain.entity.completed_order import CompletedOrder
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.completed_order import (
    CompletedOrderID,
    PaypalReceivedAmount,
    UserReceivedAmount,
    ReceivedAt,
    TakenCommission,
)
from src.infrastructure.data.models import CompletedOrderModel


class CompletedOrderDAL(BaseCompletedOrderDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, completed_order: CompletedOrder) -> None:
        query = insert(CompletedOrderModel).values(
            order_id=completed_order.order_id.value,
            paypal_received_amount=completed_order.paypal_received_amount.value,
            user_received_amount=completed_order.user_received_amount.value,
            received_at=completed_order.received_at.value,
            taken_commission=completed_order.taken_commission.value,
        )
        await self._session.execute(query)
        await self._session.commit()

    async def get(self, completed_order_id: CompletedOrderID) -> Optional[CompletedOrder]:
        query = select(CompletedOrderModel)
        result = await self._session.execute(query)
        completed_order = result.scalar_one_or_none()

        return CompletedOrder(
            order_id=OrderID(completed_order.order_id),
            paypal_received_amount=PaypalReceivedAmount(completed_order.paypal_received_amount),
            user_received_amount=UserReceivedAmount(completed_order.user_received_amount),
            received_at=ReceivedAt(completed_order.received_at),
            taken_commission=TakenCommission(completed_order.taken_commission),
        )
