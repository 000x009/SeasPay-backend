from dataclasses import dataclass
from typing import List

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class LoginData(ValueObject[List[str]]):
    value: List[str]
