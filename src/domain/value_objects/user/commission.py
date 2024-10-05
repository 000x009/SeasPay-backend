from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.user import EmptyValueError, WithdrawAmountError
from src.infrastructure.config import load_settings

class Commission(ValueObject[int]):
    value: int

    def _validate(self) -> None:
        settings = load_settings()
        if not self.value:
            raise EmptyValueError('Commission value is empty.')
        if self.value < settings.commission.paypal.min_percentage_to_withdraw:
            raise WithdrawAmountError('Commission value is less than minimum percentage to withdraw.')
        if self.value > settings.commission.paypal.max_percentage_to_withdraw:
            raise WithdrawAmountError('Commission value is greater than maximum percentage to withdraw.')
