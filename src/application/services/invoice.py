from src.infrastructure.dal import InvoiceDAL
from src.application.dto.invoice import InvoiceDTO, GetInvoiceDTO, UpdateInvoiceDTO
from src.domain.entity.invoice import Invoice
from src.domain.value_objects.invoice import InvoiceID, CreatedAt
from src.domain.value_objects.order import OrderID


class InvoiceService:
    def __init__(self, invoice_dal: InvoiceDAL):
        self._invoice_dal = invoice_dal

    async def get(self, data: GetInvoiceDTO) -> InvoiceDTO:
        invoice = await self._invoice_dal.get(InvoiceID(data.id))

        return InvoiceDTO(
            id=invoice.invoice_id.value,
            order_id=invoice.order_id.value,
            status=invoice.status,
            created_at=invoice.created_at,
        )

    async def update(self, data: UpdateInvoiceDTO) -> None:
        invoice = await self.get(GetInvoiceDTO(id=data.id))

        await self._invoice_dal.update(
            invoice_id=InvoiceID(data.id),
            invoice=Invoice(
                invoice_id=InvoiceID(invoice.id),
                order_id=OrderID(invoice.order_id),
                status=data.status,
                created_at=CreatedAt(invoice.created_at),
            )
        )
    