from typing import Optional
from decimal import Decimal
from datetime import timedelta

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseCompletedOrderDAL
from src.domain.entity.completed_order import CompletedOrder
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.completed_order import (
    CompletedOrderID,
    PaypalReceivedAmount,
    UserReceivedAmount,
    CompletedAt,
)
from src.infrastructure.data.models import CompletedOrderModel
from src.domain.value_objects.statistics import TimeSpan


class CompletedOrderDAL(BaseCompletedOrderDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(self, completed_order: CompletedOrder) -> None:
        query = insert(CompletedOrderModel).values(
            order_id=completed_order.order_id.value,
            paypal_received_amount=completed_order.paypal_received_amount.value if completed_order.paypal_received_amount else None,
            user_received_amount=completed_order.user_received_amount.value if completed_order.user_received_amount else None,
            completed_at=completed_order.completed_at.value,
        )
        await self._session.execute(query)

    async def get(self, completed_order_id: CompletedOrderID) -> Optional[CompletedOrder]:
        query = select(CompletedOrderModel).where(CompletedOrderModel.id == completed_order_id.value)
        result = await self._session.execute(query)
        completed_order = result.scalar_one_or_none()

        return CompletedOrder(
            order_id=OrderID(completed_order.order_id),
            paypal_received_amount=PaypalReceivedAmount(completed_order.paypal_received_amount),
            user_received_amount=UserReceivedAmount(completed_order.user_received_amount),
            completed_at=CompletedAt(completed_order.completed_at),
        )

    async def count_total_withdraw(self) -> Decimal:
        query = select(func.sum(CompletedOrderModel.paypal_received_amount))
        result = await self._session.execute(query)
        total_user_received = result.scalar_one_or_none()

        return Decimal(total_user_received or 0)

    async def count_profit(self, timespan: Optional[TimeSpan] = None) -> Decimal:
        if timespan is None:
            query = (
                select(func.sum(CompletedOrderModel.paypal_received_amount - CompletedOrderModel.user_received_amount))
            )
        else:
            query = (
                select(
                    func.sum(CompletedOrderModel.paypal_received_amount - CompletedOrderModel.user_received_amount)
                )
                .filter(CompletedOrderModel.completed_at > func.now() - timedelta(days=timespan.value))
            )
        result = await self._session.execute(query)
        total_profit = result.scalar_one_or_none()

        return Decimal(total_profit or 0)
