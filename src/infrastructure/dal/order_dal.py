from typing import List, Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseOrderDAL
from src.application.dto.order import OrderDTO
from src.domain.entity.order import Order
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.user import UserID
from src.infrastructure.data.models import OrderModel


class OrderDAL(BaseOrderDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_(
        self, user_id: UserID, limit: int, offset: int
    ) -> Optional[List[OrderDTO]]:
        query = (
            select(OrderModel)
            .filter_by(
                user_id=user_id.value,
            )
            .limit(limit + 1)
            .offset(offset)
            .order_by(OrderModel.time)
        )

        result = await self._session.execute(query)
        orders = result.scalars().all()
        if not orders:
            return None

        return [
            OrderDTO(
                id=order.id,
                user_id=order.user_id,
                invoice_id=order.invoice_id,
                payment_receipt=order.payment_receipt,
                final_amount=order.final_amount,
                status=order.status,
                time=order.time,
            )
            for order in orders
        ]

    async def get(
        self, user_id: UserID, order_id: OrderID,
    ) -> Optional[OrderDTO]:
        query = select(OrderModel).filter_by(
            user_id=user_id.value,
            id=order_id.value,
        )
        result = await self._session.execute(query)
        order = result.scalar_one_or_none()
        if not order:
            return None

        return OrderDTO(
            id=order.id,
            user_id=order.user_id,
            invoice_id=order.invoice_id,
            payment_receipt=order.payment_receipt,
            final_amount=order.final_amount,
            time=order.time,
            status=order.status,
        )

    async def create(self, order: Order) -> None:
        query = insert(OrderModel).values(
            user_id=order.user_id.value,
            invoice_id=order.invoice_id.value,
            payment_receipt=order.payment_receipt.value,
            final_amount=order.final_amount.value,
            time=order.time.value,
            status=order.status,
        )
        await self._session.execute(query)
        await self._session.commit()
