from src.infrastructure.dal.withdraw_details_dal import WithdrawDetailsDAL
from src.application.dto.withdraw_details import (
    AddWithdrawDetailsDTO,
    GetWithdrawDetailsDTO,
    WithdrawDetailsDTO,
    CalculateWithdrawCommissionDTO,
    WithdrawCalculationsDTO,
)
from src.domain.value_objects.withdraw_method import (
    PaymentReceipt,
    WithdrawCommission,
)
from src.domain.entity.withdraw_details import WithdrawDetails
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.requisite import RequisiteId
from src.domain.exceptions.withdraw_details import WithdrawDetailsNotFound
from src.application.common.uow import UoW
from src.domain.entity.completed_order import PaymentSystemReceivedAmount


class WithdrawService:
    def __init__(
        self,
        dal: WithdrawDetailsDAL,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.uow = uow

    async def add_details(self, data: AddWithdrawDetailsDTO) -> WithdrawDetailsDTO:
        method = WithdrawDetails(
            order_id=OrderID(data.order_id),
            requisite_id=RequisiteId(data.requisite_id),
            payment_receipt=PaymentReceipt(data.payment_receipt),
            commission=WithdrawCommission(data.commission),
        )
        withdraw_method = await self.dal.insert(method)
        await self.uow.commit()

        return WithdrawDetailsDTO(
            order_id=withdraw_method.order_id.value,
            requisite_id=withdraw_method.requisite_id.value,
            payment_receipt=withdraw_method.payment_receipt.value,
            commission=withdraw_method.commission.value,
        )

    async def get_withdraw_method(self, data: GetWithdrawDetailsDTO) -> WithdrawDetailsDTO:
        method = await self.dal.get(OrderID(data.order_id))
        if method is None:
            raise WithdrawDetailsNotFound(f"Withdraw method not found for order: {data.order_id}")
        
        return WithdrawDetailsDTO(
            order_id=method.order_id.value,
            requisite_id=method.requisite_id.value,
            payment_receipt=method.payment_receipt.value,
            commission=method.commission.value,
        )

    async def calculate_commission(self, data: CalculateWithdrawCommissionDTO) -> WithdrawCalculationsDTO:
        withdraw_details = await self.get_withdraw_method(GetWithdrawDetailsDTO(order_id=data.order_id))
        withdraw_details = WithdrawDetails(
            order_id=OrderID(withdraw_details.order_id),
            requisite_id=RequisiteId(withdraw_details.requisite_id),
            payment_receipt=PaymentReceipt(withdraw_details.payment_receipt),
            commission=WithdrawCommission(withdraw_details.commission),
        )
        user_must_receive = withdraw_details.calculate_amount_user_must_receive(
            PaymentSystemReceivedAmount(data.payment_system_received_amount)
        )

        return WithdrawCalculationsDTO(
            withdraw_commission=withdraw_details.commission.value,
            recipient_must_receive=user_must_receive.value,
        )
