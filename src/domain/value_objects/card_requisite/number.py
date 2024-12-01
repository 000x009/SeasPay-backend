from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.card_requisite import CardNumberError

class Number(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        cleaned = ''.join(filter(str.isdigit, self.value))
        
        if len(cleaned) != 16:
            raise CardNumberError("Card number must be exactly 16 digits")
        if not cleaned.isdigit():
            raise CardNumberError("Card number must contain only digits")
