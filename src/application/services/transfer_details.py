from src.infrastructure.dal.tranfer_details import TransferDetailsDAL
from src.application.dto.transfer_details import (
    AddTransferDetailsDTO,
    GetTransferDetailsDTO,
    TransferDetailsDTO,
    CalculateTransferCommissionDTO,
    CalculationsDTO,
)
from src.domain.value_objects.transfer_details import (
    ReceiptPhotoURL,
    ReceiverEmail,
    TransferAmount,
    Commission,
)
from src.domain.value_objects.completed_order import PaymentSystemReceivedAmount
from src.domain.entity.transfer_details import TransferDetails
from src.domain.value_objects.order import OrderID
from src.domain.exceptions.transfer_details import TransferDetailsNotFound
from src.application.common.uow import UoW


class TransferDetailsService:
    def __init__(
        self,
        dal: TransferDetailsDAL,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.uow = uow

    async def add_details(self, data: AddTransferDetailsDTO) -> TransferDetailsDTO:
        details = TransferDetails(
            order_id=OrderID(data.order_id),
            receiver_email=ReceiverEmail(data.receiver_email),
            receipt_photo_url=ReceiptPhotoURL(data.receipt_photo_url),
            amount=TransferAmount(data.amount),
            commission=Commission(data.commission),
        )
        transfer_details = await self.dal.insert(details)
        await self.uow.commit()

        return TransferDetailsDTO(
            order_id=transfer_details.order_id.value,
            receiver_email=transfer_details.receiver_email.value,
            receipt_photo_url=transfer_details.receipt_photo_url.value,
            amount=transfer_details.amount.value,
            commission=transfer_details.commission.value,
        )

    async def get_details(self, data: GetTransferDetailsDTO) -> TransferDetailsDTO:
        transfer_details = await self.dal.get(OrderID(data.order_id))
        if transfer_details is None:
            raise TransferDetailsNotFound(f"Transfer details not found for order: {data.order_id}")

        return TransferDetailsDTO(
            order_id=transfer_details.order_id.value,
            receiver_email=transfer_details.receiver_email.value,
            receipt_photo_url=transfer_details.receipt_photo_url.value,
            amount=transfer_details.amount.value,
            commission=transfer_details.commission.value,
        )

    async def calculate_commission(self, data: CalculateTransferCommissionDTO) -> CalculationsDTO:
        transfer_details = await self.get_details(GetTransferDetailsDTO(order_id=data.order_id))
        transfer_details = TransferDetails(
            order_id=OrderID(transfer_details.order_id),
            receiver_email=ReceiverEmail(transfer_details.receiver_email),
            amount=TransferAmount(transfer_details.amount),
            receipt_photo_url=ReceiptPhotoURL(transfer_details.receipt_photo_url),
            commission=Commission(transfer_details.commission),
        )
        user_must_receive = transfer_details.calculate_amount_user_must_receive(
            PaymentSystemReceivedAmount(data.payment_system_received_amount)
        )

        return CalculationsDTO(
            transfer_commission=transfer_details.commission.value,
            recipient_must_receive=user_must_receive.value,
        )
