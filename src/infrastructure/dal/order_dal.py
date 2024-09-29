from typing import List, Optional

from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseOrderDAL
from src.application.dto.order import OrderDTO
from src.domain.entity.order import Order
from src.domain.value_objects.order import OrderID, PaymentReceipt, FinalAmount, CreatedAt
from src.domain.value_objects.user import UserID
from src.domain.value_objects.invoice import InvoiceID
from src.infrastructure.data.models import OrderModel


class OrderDAL(BaseOrderDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_(
        self, user_id: UserID, limit: int, offset: int
    ) -> Optional[List[Order]]:
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
            Order(
                id=OrderID(order.id),
                user_id=UserID(order.user_id),
                payment_receipt=PaymentReceipt(order.payment_receipt),
                created_at=CreatedAt(order.created_at),
                status=order.status,
                telegram_message_id=order.telegram_message_id,
            )
            for order in orders
        ]

    async def get(self, order_id: OrderID) -> Optional[Order]:
        query = select(OrderModel).filter_by(id=order_id.value)
        result = await self._session.execute(query)
        order = result.scalar_one_or_none()
        if not order:
            return None
        
        return Order(
            id=OrderID(order.id),
            user_id=UserID(order.user_id),
            payment_receipt=PaymentReceipt(order.payment_receipt),
            created_at=CreatedAt(order.created_at),
            status=order.status,
            telegram_message_id=order.telegram_message_id,
        )

    async def insert(self, order: Order) -> Order:
        order_model = OrderModel(
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id,
        )
        self._session.add(order_model)
        await self._session.flush(objects=[order_model])

        return Order(
            id=OrderID(order_model.id),
            user_id=UserID(order_model.user_id),
            payment_receipt=PaymentReceipt(order_model.payment_receipt),
            created_at=CreatedAt(order_model.created_at),
            status=order.status,
            telegram_message_id=order.telegram_message_id,
        )

    async def update(self, order: Order) -> Optional[Order]:
        order_model = OrderModel(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            created_at=order.created_at.value,
            status=order.status.value,
            telegram_message_id=order.telegram_message_id,
        )
        await self._session.flush(objects=[order_model])
        await self._session.commit()

        return order