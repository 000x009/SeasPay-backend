from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.application.common.dal.transfer_details import BaseTransferDetailsDAL
from src.domain.entity.transfer_details import TransferDetails
from src.domain.value_objects.order import OrderID
from src.domain.value_objects.transfer_details import (
    TransferAmount,
    ReceiptPhotoURL,
    ReceiverEmail,
    Commission,
)
from src.infrastructure.data.models import TransferDetailsModel


class TransferDetailsDAL(BaseTransferDetailsDAL):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, transfer_details: TransferDetails) -> TransferDetails:
        model = TransferDetailsModel(
            order_id=transfer_details.order_id.value,
            receiver_email=transfer_details.receiver_email.value,
            amount=transfer_details.amount.value,
            receipt_photo_url=transfer_details.receipt_photo_url.value,
            commission=transfer_details.commission.value,
        )
        self.session.add(model)

        return TransferDetails(
            order_id=OrderID(model.order_id),
            receiver_email=ReceiverEmail(model.receiver_email),
            amount=TransferAmount(model.amount),
            receipt_photo_url=ReceiptPhotoURL(model.receipt_photo_url),
            commission=Commission(model.commission),
        )

    async def get(self, order_id: OrderID) -> Optional[TransferDetails]:
        query = select(TransferDetailsModel).filter_by(order_id=order_id.value)
        result = await self.session.execute(query)
        db_withdraw_method = result.scalar_one_or_none()
        if db_withdraw_method is None:
            return None

        return TransferDetails(
            order_id=OrderID(db_withdraw_method.order_id),
            receiver_email=ReceiverEmail(db_withdraw_method.receiver_email),
            amount=TransferAmount(db_withdraw_method.amount),
            receipt_photo_url=ReceiptPhotoURL(db_withdraw_method.receipt_photo_url),
            commission=Commission(db_withdraw_method.commission),
        )
