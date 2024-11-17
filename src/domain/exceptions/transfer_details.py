from src.domain.exceptions.base import DomainError


class TransferDetailsDataError(DomainError):
    pass


class ReceiverEmailError(TransferDetailsDataError):
    pass


class TransferDetailsNotFound(DomainError):
    pass
