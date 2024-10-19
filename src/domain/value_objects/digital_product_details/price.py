from dataclasses import dataclass
from decimal import Decimal

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class ProductPrice(ValueObject[Decimal]):
    """Price in USD"""

    value: Decimal
