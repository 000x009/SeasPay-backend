from src.domain.common.value_objects import ValueObject


class InvoiceURL(ValueObject[str]):
    value: str
