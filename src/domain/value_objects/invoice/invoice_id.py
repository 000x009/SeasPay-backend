from src.domain.common.value_objects import ValueObject


class InvoiceID(ValueObject[str]):
    value: str
