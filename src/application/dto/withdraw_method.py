from dataclasses import dataclass

from src.domain.value_objects.withdraw_method import MethodEnum


@dataclass(frozen=True)
class WithdrawMethodDTO:
    id: int
    order_id: int
    method: MethodEnum


@dataclass(frozen=True)
class CardMethodDTO(WithdrawMethodDTO):
    card_number: str
    card_holder_name: str


@dataclass(frozen=True)
class CryptoMethodDTO(WithdrawMethodDTO):
    crypto_address: str
    network: str


@dataclass(frozen=True)
class AddWithdrawMethodDTO:
    order_id: int
    method: MethodEnum


@dataclass(frozen=True)
class AddCardMethodDTO(AddWithdrawMethodDTO):
    card_number: str
    card_holder_name: str


@dataclass(frozen=True)
class AddCryptoMethodDTO(AddWithdrawMethodDTO):
    crypto_address: str
    network: str


@dataclass(frozen=True)
class GetWithdrawMethodDTO:
    order_id: int
