from src.domain.common.value_objects import ValueObject


class WalletAddress(ValueObject[str]):
    value: str
