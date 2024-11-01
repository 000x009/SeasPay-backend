from dataclasses import dataclass
from decimal import Decimal

from src.domain.common.value_objects import ValueObject
from src.infrastructure.config import app_settings
from src.domain.exceptions.user_commission import WrongCommissionError


@dataclass(frozen=True)
class UserDigitalProductCommission(ValueObject[Decimal]):
    """An amount of money in USD"""

    value: Decimal

    def _validate(self) -> None:
        digital_product_commission = app_settings.commission.digital_product_usd_amount_commission
        if self.value != digital_product_commission:
            raise WrongCommissionError(
                f'Commission must be an amount of {digital_product_commission} USD. Input: {self.value}'
            )
