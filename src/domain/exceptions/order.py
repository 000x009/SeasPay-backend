from src.domain.exceptions.base import DomainError


class OrderNotFoundError(DomainError):
    pass


class OrderAlreadyTakenError(DomainError):
    pass
