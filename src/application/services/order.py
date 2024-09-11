from typing import Optional, List

from src.infrastructure.dal import OrderDAL
from src.application.dto.order import (
    ListOrderDTO,
    OrderDTO,
    GetOrderDTO,
    CreateOrderDTO,
    TakeOrderDTO,
    AddTelegramMessageIdDTO,
)
from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import OrderID, CreatedAt, PaymentReceipt, OrderStatus
from src.domain.entity.order import Order
from src.domain.exceptions.order import OrderNotFoundError, OrderAlreadyTakenError
from src.domain.value_objects.order_message import MessageID


class OrderService:
    def __init__(self, order_dal: OrderDAL) -> None:
        self._order_dal = order_dal

    async def list_(self, data: ListOrderDTO) -> Optional[List[OrderDTO]]:
        return await self._order_dal.list_(
            user_id=UserID(data.user_id),
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )

    async def get(self, data: GetOrderDTO) -> Optional[OrderDTO]:
        order = await self._order_dal.get(OrderID(data.order_id))
        if not order:
            return None

        return OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            created_at=order.created_at.value,
            status=order.status,
        )

    async def create(self, data: CreateOrderDTO) -> OrderDTO:
        order = await self._order_dal.insert(
            Order(
                user_id=UserID(data.user_id),
                payment_receipt=PaymentReceipt(data.payment_receipt),
                created_at=CreatedAt(data.created_at),
                status=data.status,
            )
        )

        return OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            created_at=order.created_at.value,
            status=order.status,
        )
    
    async def take_order(self, data: TakeOrderDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))

        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")
        if order.status not in (OrderStatus.NEW, OrderStatus.DELAY):
            raise OrderAlreadyTakenError(f"Order with id {data.order_id} already taken.")

        order.status = OrderStatus.PROCESSING
        updated_order = await self._order_dal.update(order)

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status,
        )

    async def add_telegram_message_id(self, data: AddTelegramMessageIdDTO) -> OrderDTO:
        order = await self._order_dal.get(OrderID(data.order_id))   
        if not order:
            raise OrderNotFoundError(f"Order with id {data.order_id} not found.")

        order.telegram_message_id = MessageID(data.telegram_message_id)
        updated_order = await self._order_dal.update(order)

        return OrderDTO(
            id=updated_order.id.value,
            user_id=updated_order.user_id.value,
            payment_receipt=updated_order.payment_receipt.value,
            created_at=updated_order.created_at.value,
            status=updated_order.status,
            telegram_message_id=updated_order.telegram_message_id.value,
        )