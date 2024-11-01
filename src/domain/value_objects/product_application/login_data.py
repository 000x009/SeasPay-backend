from typing import Sequence
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class LoginData(ValueObject[Sequence[str]]):
    value: Sequence[str]
