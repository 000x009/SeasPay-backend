from enum import Enum


class InvoiceStatus(Enum):
    SEND = 'SEND'
    DRAFT = 'DRAFT'
    DELETE = 'DELETE'
