from src.domain.common.value_objects import ValueObject


class Network(ValueObject[str]):
    value: str
