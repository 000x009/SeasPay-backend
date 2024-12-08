from aiocryptopay.const import CurrencyType

from src.application.common.dal.payment import PaymentDAL
from src.domain.entity.payment import Payment
from src.domain.value_objects.payment import Amount, InvoiceURL
from src.application.common.uow import UoW
from src.application.dto.payment import CreatePaymentDTO, PaymentDTO
from src.domain.value_objects.user import UserID
from src.application.services.cryptopay import CryptopayService
from src.application.dto.cryptopay import CreateInvoiceDTO


class PaymentService:
    def __init__(
        self,
        dal: PaymentDAL,
        uow: UoW,
        cryptopay: CryptopayService,
    ) -> None:
        self.dal = dal
        self.uow = uow
        self.cryptopay = cryptopay

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
