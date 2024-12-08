from dataclasses import dataclass
from aiocryptopay.const import CurrencyType as CryptoPayCurrencyType

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class CurrencyType(ValueObject[CryptoPayCurrencyType]):
    value: CryptoPayCurrencyType
