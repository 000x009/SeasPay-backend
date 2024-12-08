from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.payment import PaymentDAL
from src.domain.entity.payment import Payment
from src.domain.value_objects.payment import PaymentID
from src.infrastructure.data.models import PaymentModel
from src.domain.value_objects.user import UserID
from src.domain.value_objects.payment import PaymentStatus, CreatedAt, InvoiceURL, Amount


class PaymentDALImpl(PaymentDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, payment_id: PaymentID) -> Optional[Payment]:
        query = select(PaymentModel).filter_by(id=payment_id.value)
        result = await self.session.execute(query)
        payment = result.scalar_one_or_none()
        if not payment:
            return None
        
        return Payment(
            id=PaymentID(payment.id),
            user_id=UserID(payment.user_id),
            invoice_url=InvoiceURL(payment.invoice_url),
            created_at=CreatedAt(payment.created_at),
            status=PaymentStatus(payment.status),
            amount=Amount(payment.amount),
        )

    async def insert(self, payment: Payment) -> Payment:
        payment_model = PaymentModel(
            id=payment.id.value,
            user_id=payment.user_id.value,
            invoice_url=payment.invoice_url.value if payment.invoice_url else None,
            created_at=payment.created_at.value,
            status=payment.status.value.value,
            amount=payment.amount.value,
        )
        self.session.add(payment_model)

        return Payment(
            id=PaymentID(payment_model.id),
            user_id=UserID(payment_model.user_id),
            invoice_url=InvoiceURL(payment_model.invoice_url),
            created_at=CreatedAt(payment_model.created_at),
            status=PaymentStatus(payment_model.status),
            amount=Amount(payment_model.amount),
        )

    async def update(self, payment: Payment) -> Payment:
        payment_model = PaymentModel(
            id=payment.id.value,
            user_id=payment.user_id.value,
            invoice_url=payment.invoice_url.value,
            created_at=payment.created_at.value,
            status=payment.status.value,
            amount=payment.amount.value,
        )
        await self.session.merge(payment_model)

        return payment
