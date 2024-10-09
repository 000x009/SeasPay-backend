from typing import Optional

from src.infrastructure.dal import CompletedOrderDAL
from src.application.dto.completed_order import (
    CompletedOrderDTO,
    AddCompletedOrderDTO,
    GetCompletedOrderDTO,
    TotalWithdrawDTO,
    ProfitDTO,
)
from src.domain.entity.completed_order import CompletedOrder
from src.domain.value_objects.completed_order import (
    CompletedOrderID,
    PaypalReceivedAmount,
    UserReceivedAmount,
    CompletedAt,
)
from src.domain.value_objects.order import OrderID


class CompletedOrderService:
    def __init__(self, completed_order_dal: CompletedOrderDAL):
        self._dal = completed_order_dal

    async def add(self, data: AddCompletedOrderDTO) -> None:
        await self._dal.insert(CompletedOrder(
            order_id=OrderID(data.order_id),
            paypal_received_amount=PaypalReceivedAmount(data.paypal_received_amount),
            user_received_amount=UserReceivedAmount(data.user_received_amount),
            completed_at=CompletedAt(data.completed_at),
        ))

    async def get(self, data: GetCompletedOrderDTO) -> Optional[CompletedOrderDTO]:
        completed_order = await self._dal.get(CompletedOrderID(data.id))
        if not completed_order:
            return None

        return CompletedOrderDTO(
            order_id=completed_order.order_id.value,
            paypal_received_amount=completed_order.paypal_received_amount.value,
            user_received_amount=completed_order.user_received_amount.value,
            completed_at=completed_order.completed_at.value,
        )

    async def count_total_withdraw(self) -> TotalWithdrawDTO:
        total_withdraw = await self._dal.count_total_withdraw()

        return TotalWithdrawDTO(
            total_withdraw=total_withdraw,
        )

    async def count_profit(self) -> ProfitDTO:
        profit = await self._dal.count_profit()

        return ProfitDTO(
            profit=profit,
        )

