from src.domain.common.value_objects import ValueObject


class Memo(ValueObject[str]):
    value: str
