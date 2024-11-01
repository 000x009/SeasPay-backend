from typing import Dict
from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class LoginData(ValueObject[Dict[str, str]]):
    value: Dict[str, str]
