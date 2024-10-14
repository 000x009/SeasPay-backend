from src.domain.exceptions.base import DomainError


class WithdrawDetailsNotFound(DomainError):
    pass


class CardNumberError(DomainError):
    pass


class CardHolderNameError(DomainError):
    pass


class CryptoAddressError(DomainError):
    pass


class CryptoNetworkError(DomainError):
    pass
