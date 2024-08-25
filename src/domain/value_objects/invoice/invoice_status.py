from enum import Enum


class InvoiceStatus(Enum):
    SENT = 'SENT'
    PAID = 'PAID'
    DELETED = 'DELETED'
