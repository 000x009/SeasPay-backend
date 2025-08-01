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
    PaymentSystemReceivedAmount,
    UserReceivedAmount,
    CompletedAt,
)
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.statistics import TimeSpan
from src.application.common.uow import UoW
from src.domain.exceptions.completed_order import CompletedOrderNotFoundError


class CompletedOrderService:
    def __init__(
        self,
        completed_order_dal: CompletedOrderDAL,
        uow: UoW,
    ):
        self._dal = completed_order_dal
        self.uow = uow

    async def add(self, data: AddCompletedOrderDTO) -> None:
        await self._dal.insert(CompletedOrder(
            order_id=OrderID(data.order_id),
            payment_system_received_amount=PaymentSystemReceivedAmount(data.payment_system_received_amount)
            if data.payment_system_received_amount else None,
            user_received_amount=UserReceivedAmount(data.user_received_amount) if data.user_received_amount else None,
            completed_at=CompletedAt(data.completed_at),
        ))
        await self.uow.commit()

    async def get(self, data: GetCompletedOrderDTO) -> Optional[CompletedOrderDTO]:
        completed_order = await self._dal.get(CompletedOrderID(data.order_id))
        if not completed_order:
            raise CompletedOrderNotFoundError(f"Completed order details not found for order: <{data.order_id}>")

        return CompletedOrderDTO(
            order_id=completed_order.order_id.value,
            payment_system_received_amount=completed_order.payment_system_received_amount.value,
            user_received_amount=completed_order.user_received_amount.value,
            completed_at=completed_order.completed_at.value,
        )

    async def count_total_withdraw(self) -> TotalWithdrawDTO:
        total_withdraw = await self._dal.count_total_withdraw()

        return TotalWithdrawDTO(
            total_withdraw=total_withdraw,
        )

    async def count_statistics_profit(self) -> ProfitDTO:
        all_time_profit = await self._dal.count_profit()
        month_profit = await self._dal.count_profit(TimeSpan(30))
        week_profit = await self._dal.count_profit(TimeSpan(7))

        return ProfitDTO(
            all_time=all_time_profit,
            month=month_profit,
            week=week_profit,
        )
