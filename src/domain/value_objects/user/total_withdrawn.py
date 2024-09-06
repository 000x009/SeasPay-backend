from decimal import Decimal

from src.domain.common.value_objects import ValueObject
from src.domain.exceptions.user import EmptyValueError


class TotalWithdrawn(ValueObject[Decimal]):
    value: Decimal

    # def _validate(self) -> None:
    #     if not self.value:
    #         raise EmptyValueError('Total withdrawn value is empty.')
