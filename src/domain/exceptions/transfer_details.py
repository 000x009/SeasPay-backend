from src.domain.exceptions.base import DomainError


class ReceiverEmailError(DomainError):
    pass


class TransferDetailsNotFound(DomainError):
    pass
