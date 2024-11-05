from dataclasses import dataclass

from src.domain.common.value_objects import ValueObject


@dataclass(frozen=True)
class ObjectURL(ValueObject[str]):
    value: str

    def get_key(self) -> str:
        return self.value.split('/')[-1]
    
    def get_bucket(self) -> str:
        return self.value.split('/')[-2]
