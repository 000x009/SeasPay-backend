from aiocryptopay.const import CurrencyType

from src.application.common.dal.payment import PaymentDAL
from src.domain.entity.payment import Payment
from src.domain.value_objects.payment import Amount, InvoiceURL, PaymentID, PaymentStatus, PaymentStatusEnum
from src.application.common.uow import UoW
from src.application.dto.payment import (
    CreatePaymentDTO,
    PaymentDTO,
    GetPaymentDTO,
    ReceivePaymentDTO,
)
from src.domain.value_objects.user import UserID
from src.application.services.cryptopay import CryptopayService
from src.application.services.order import OrderService
from src.application.dto.cryptopay import CreateInvoiceDTO
from src.domain.exceptions.payment import PaymentNotFoundError
from src.application.dto.order import PayOrderDTO


class PaymentService:
    def __init__(
        self,
        dal: PaymentDAL,
        uow: UoW,
        cryptopay: CryptopayService,
        order_service: OrderService,
    ) -> None:
        self.dal = dal
        self.uow = uow
        self.cryptopay = cryptopay
        self.order_service = order_service

    async def create(self, data: CreatePaymentDTO) -> PaymentDTO:
        payment = await self.dal.insert(Payment(
            user_id=UserID(data.user_id),
            amount=Amount(data.amount),
        ))
        invoice = await self.cryptopay.create(CreateInvoiceDTO(
            payment_id=payment.id.value,
            amount=payment.amount.value,
            currency_type=CurrencyType.CRYPTO,
            asset="USDT",
        ))
        payment.invoice_url = InvoiceURL(invoice.url)
        updated_payment = await self.dal.update(payment)
        await self.uow.commit()

        return PaymentDTO(
            id=updated_payment.id.value,
            user_id=updated_payment.user_id.value,
            invoice_url=updated_payment.invoice_url.value,
            amount=updated_payment.amount.value,
            status=updated_payment.status.value,
            created_at=updated_payment.created_at.value,
        )

    async def get(self, data: GetPaymentDTO) -> PaymentDTO:
        payment = await self.dal.get(PaymentID(data.payment_id))
        if not payment:
            raise PaymentNotFoundError(f"Payment not found: <{data.payment_id}>")

        return PaymentDTO(
            id=payment.id.value,
            user_id=payment.user_id.value,
            invoice_url=payment.invoice_url.value,
            amount=payment.amount.value,
            status=payment.status.value,
            created_at=payment.created_at.value,
        )

    async def receive_payment(self, data: ReceivePaymentDTO) -> None:
        payment = await self.dal.get(PaymentID(data.payment_id))
        if not payment:
            raise PaymentNotFoundError(f"Payment not found: <{data.payment_id}>")
        
        print(payment.status.value)
        if payment.status.value == PaymentStatusEnum.ACTIVE.value:
            await self.order_service.pay_order(PayOrderDTO(payment_id=payment.id.value))
            payment.status = PaymentStatus(PaymentStatusEnum.PAID)
            payment = await self.dal.update(payment)
            await self.uow.commit()

        return PaymentDTO(
            id=payment.id.value,
            user_id=payment.user_id.value,
            invoice_url=payment.invoice_url.value,
            amount=payment.amount.value,
            status=payment.status.value,
            created_at=payment.created_at.value,
        )
