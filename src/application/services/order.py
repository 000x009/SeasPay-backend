from typing import Optional, List

from src.infrastructure.dal import OrderDAL
from src.application.dto.order import ListOrderDTO, OrderDTO, GetOrderDTO, CreateOrderDTO
from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import OrderID, CreatedAt, PaymentReceipt, FinalAmount
from src.domain.value_objects.invoice import InvoiceID
from src.domain.entity.order import Order


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
        return await self._order_dal.get(
            user_id=UserID(data.user_id),
            order_id=OrderID(data.order_id),
        )


    async def create(self, data: CreateOrderDTO) -> OrderDTO:
        order = await self._order_dal.insert(
            Order(
                user_id=UserID(data.user_id),
                payment_receipt=PaymentReceipt(data.payment_receipt),
                final_amount=FinalAmount(data.final_amount),
                created_at=CreatedAt(data.created_at),
                status=data.status,
            )
        )

        return OrderDTO(
            id=order.id.value,
            user_id=order.user_id.value,
            payment_receipt=order.payment_receipt.value,
            final_amount=order.final_amount.value,
            created_at=order.created_at.value,
            status=order.status,
        )
