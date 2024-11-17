from src.domain.exceptions.base import DomainError


class CompletedOrderDataError(DomainError):
    pass


class InvalidTakenCommissionError(CompletedOrderDataError):
    pass


class InvalidUserReceivedAmountError(CompletedOrderDataError):
    pass


class InvalidPaypalReceivedAmountError(CompletedOrderDataError):
    pass


class CompletedOrderNotFoundError(DomainError):
    pass
