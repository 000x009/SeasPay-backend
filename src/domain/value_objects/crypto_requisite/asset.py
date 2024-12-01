from src.domain.common.value_objects import ValueObject


class Asset(ValueObject[str]):
    value: str
