from src.domain.exceptions.base import DomainError


class WrongCommissionError(DomainError):
    pass


class UserCommissionNotFoundError(DomainError):
    pass
