from src.domain.exceptions.base import DomainError


class CardRequisiteValidationError(DomainError):
    pass


class CardNumberError(CardRequisiteValidationError):
    pass

