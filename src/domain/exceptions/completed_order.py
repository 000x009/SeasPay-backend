from src.domain.exceptions.base import DomainError


class InvalidTakenCommissionError(DomainError):
    pass


class InvalidUserReceivedAmountError(DomainError):
    pass


class InvalidPaypalReceivedAmountError(DomainError):
    pass


class CompletedOrderNotFoundError(DomainError):
    pass
