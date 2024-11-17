from src.domain.exceptions.base import DomainError


class WithdrawDetailsDataError(DomainError):
    pass


class WithdrawDetailsNotFound(DomainError):
    pass


class CardNumberError(WithdrawDetailsDataError):
    pass


class CardHolderNameError(WithdrawDetailsDataError):
    pass


class CryptoAddressError(WithdrawDetailsDataError):
    pass


class CryptoNetworkError(WithdrawDetailsDataError):
    pass
