from src.domain.exceptions import DomainError, ValueObjectError


class NotAuthorizedError(DomainError):
    pass


class EmptyValueError(ValueObjectError):
    pass


class UserNotFoundError(DomainError):
    pass
