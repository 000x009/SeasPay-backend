from typing import Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.data.models import InvoiceModel
from src.application.common.dal import BaseInvoiceDAL
from src.domain.entity.invoice import Invoice
from src.domain.value_objects.invoice import InvoiceID, CreatedAt
from src.domain.value_objects.order import OrderID


class InvoiceDAL(BaseInvoiceDAL):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, invoice_id: InvoiceID) -> Optional[Invoice]:
        query = select(InvoiceModel).filter_by(id=invoice_id.value)
        result = await self._session.execute(query)
        invoice = result.scalar_one()

        if not invoice:
            return None

        return Invoice(
            invoice_id=InvoiceID(invoice.id),
            order_id=OrderID(invoice.order_id),
            status=invoice.status,
            created_at=CreatedAt(invoice.created_at),
        )

    async def add(self, invoice: Invoice) -> None:
        query = insert(InvoiceModel).values(
            id=invoice.invoice_id.value,
            order_id=invoice.order_id.value,
            status=invoice.status,
            created_at=invoice.created_at,
        )
        await self._session.execute(query)
        await self._session.commit()

    async def update(self, invoice_id: InvoiceID, invoice: Invoice) -> None:
        query = update(InvoiceModel).filter_by(id=invoice_id.value).values(
            status=invoice.status,
        )
        await self._session.execute(query)
        await self._session.commit()
