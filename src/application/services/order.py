from typing import Optional, List

from src.infrastructure.dal import OrderDAL
from src.application.dto.order import ListOrderDTO, OrderDTO, GetOrderDTO, CreateOrderDTO
from src.domain.value_objects.user import UserID
from src.domain.value_objects.order import OrderID


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


    async def create(self, data: CreateOrderDTO) -> None:
        await self._order_dal