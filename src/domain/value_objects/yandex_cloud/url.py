from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class ObjectURL(ValueObject[str]):
    value: str
