from typing import List, Optional

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import BaseOrderDAL
from src.domain.entity.order import Order
from src.domain.value_objects.order import (
    OrderID,
    PaymentReceipt,
    CreatedAt,
    OrderStatus,
    OrderStatusEnum,
    OrderType,
)
from src.domain.value_objects.order_message import MessageID
from src.domain.value_objects.user import UserID
from src.domain.value_objects.payment import PaymentID
from src.infrastructure.data.models import OrderModel


class OrderDAL(BaseOrderDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_(
        self,
        user_id: UserID,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[List[Order]]:
        if limit is not None and offset is not None:
            query = (
                select(OrderModel)
                .filter_by(
                    user_id=user_id.value,
                )
                .limit(limit.value)
                .offset(offset.value)
                .order_by(desc(OrderModel.created_at))
            )
        else:
            query = (
                select(OrderModel)
                .filter_by(
                    user_id=user_id.value,
                )
                .order_by(desc(OrderModel.created_at))
            )

        result = await self._session.execute(query)
        orders = result.scalars().all()

        return [
            Order(
                id=OrderID(order.id),
                user_id=UserID(order.user_id),
                payment_receipt=PaymentReceipt(order.payment_receipt),
                payment_id=PaymentID(order.payment_id),
                created_at=CreatedAt(order.created_at),
                status=OrderStatus(order.status),
                type_=OrderType(order.type),
                telegram_message_id=MessageID(order.telegram_message_id),
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
            payment_id=PaymentID(order.payment_id),
            created_at=CreatedAt(order.created_at),
            status=OrderStatus(order.status),
            type_=OrderType(order.type),
            telegram_message_id=MessageID(order.telegram_message_id),
        )
    
    async def get_by_payment_id(self, payment_id: PaymentID) -> Optional[Order]:
        query = select(OrderModel).filter_by(payment_id=payment_id.value)
        result = await self._session.execute(query)
        order = result.scalar_one_or_none()
        if not order:
            return None
        
        return Order(
            id=OrderID(order.id),
            user_id=UserID(order.user_id),
            payment_receipt=PaymentReceipt(order.payment_receipt),
            payment_id=PaymentID(order.payment_id),
            created_at=CreatedAt(order.created_at),
            status=OrderStatus(order.status),
            type_=OrderType(order.type),
            telegram_message_id=MessageID(order.telegram_message_id),
        )

    async def insert(self, order: Order) -> Order:
        order_model = OrderModel(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            payment_id=order.payment_id.value if order.payment_id else None,
            created_at=order.created_at.value,
            status=order.status.value.value,
            type=order.type_.value,
            telegram_message_id=order.telegram_message_id.value if order.telegram_message_id else None,
        )
        self._session.add(order_model)
        await self._session.flush(objects=[order_model])

        return Order(
            id=OrderID(order_model.id),
            user_id=UserID(order_model.user_id),
            payment_receipt=PaymentReceipt(order_model.payment_receipt),
            payment_id=PaymentID(order_model.payment_id),
            created_at=CreatedAt(order_model.created_at),
            status=OrderStatus(order_model.status),
            telegram_message_id=MessageID(order_model.telegram_message_id),
            type_=OrderType(order_model.type),
        )

    async def update(self, order: Order) -> Order:
        order_model = OrderModel(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            payment_id=order.payment_id.value if order.payment_id else None,
            created_at=order.created_at.value,
            status=order.status.value,
            type=order.type_.value,
            telegram_message_id=order.telegram_message_id.value,
        )
        await self._session.merge(order_model)

        return order
    
    async def list_all(self) -> Optional[List[Order]]:
        query = select(OrderModel).order_by(OrderModel.created_at.desc())
        result = await self._session.execute(query)
        orders = result.unique().scalars().all()
        if not orders:
            return None
        
        return [Order(
            id=OrderID(order.id),
            user_id=UserID(order.user_id),
            payment_receipt=PaymentReceipt(order.payment_receipt),
            payment_id=PaymentID(order.payment_id),
            created_at=CreatedAt(order.created_at),
            status=OrderStatus(order.status),
            type_=OrderType(order.type),
            telegram_message_id=MessageID(order.telegram_message_id),
        ) for order in orders]
    
    async def get_total(self, user_id: UserID) -> int:
        query = select(func.count(OrderModel.id)).filter_by(user_id=user_id.value)
        result = await self._session.execute(query)

        return result.scalar_one()
    
    async def list_processing(self) -> Optional[List[Order]]:
        query = (
            select(OrderModel)
            .filter_by(status=OrderStatusEnum.PROCESSING.value)
            .order_by(OrderModel.created_at.desc())
        )
        result = await self._session.execute(query)
        orders = result.unique().scalars().all()
        if not orders:
            return None
        
        return [Order(
            id=OrderID(order.id),
            user_id=UserID(order.user_id),
            payment_receipt=PaymentReceipt(order.payment_receipt),
            payment_id=PaymentID(order.payment_id),
            created_at=CreatedAt(order.created_at),
            status=OrderStatus(order.status),
            type_=OrderType(order.type),
            telegram_message_id=MessageID(order.telegram_message_id),
        ) for order in orders]
    
    async def list_completed(self) -> Optional[List[Order]]:
        query = (
            select(OrderModel)
            .filter_by(status=OrderStatusEnum.COMPLETE.value)
            .order_by(OrderModel.created_at.desc())
        )
        result = await self._session.execute(query)
        orders = result.unique().scalars().all()
        if not orders:
            return None
        
        return [Order(
            id=OrderID(order.id),
            user_id=UserID(order.user_id),
            payment_receipt=PaymentReceipt(order.payment_receipt),
            payment_id=PaymentID(order.payment_id),
            created_at=CreatedAt(order.created_at),
            status=OrderStatus(order.status),
            type_=OrderType(order.type),
            telegram_message_id=MessageID(order.telegram_message_id),
        ) for order in orders]

    async def list_cancelled(self) -> Optional[List[Order]]:
        query = select(OrderModel).filter_by(status=OrderStatusEnum.CANCEL.value).order_by(OrderModel.created_at.desc())
        result = await self._session.execute(query)
        orders = result.unique().scalars().all()
        if not orders:
            return None
        
        return [Order(
            id=OrderID(order.id),
            user_id=UserID(order.user_id),
            payment_receipt=PaymentReceipt(order.payment_receipt),
            payment_id=PaymentID(order.payment_id),
            created_at=CreatedAt(order.created_at),
            status=OrderStatus(order.status),
            type_=OrderType(order.type),
            telegram_message_id=MessageID(order.telegram_message_id),
        ) for order in orders]
