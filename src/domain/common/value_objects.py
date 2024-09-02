from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, Union


V = TypeVar('V', bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """This method checks that a value is valid to create this value object"""


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[V]):
    value: V

    def __eq__(self, other: Union[ValueObject, Any]) -> bool:
        if isinstance(other, ValueObject) and other.value == self.value:
            return True
        return False

    def __ne__(self, other: Union[ValueObject, Any]) -> bool:
        return not (self.value == other.value)

    def __le__(self, other: Union[ValueObject, Any]) -> bool:
        return self.value <= other.value

    def __ge__(self, other: Union[ValueObject, Any]) -> bool:
        return self.value >= other.value
