from pydantic import BaseModel

from src.domain.value_objects.invoice import InvoiceStatus


class UpdateInvoiceStatusSchema(BaseModel):
    id: str
    status: InvoiceStatus
