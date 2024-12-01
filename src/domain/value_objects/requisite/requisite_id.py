from uuid import UUID

from src.domain.common.value_objects import ValueObject

class RequisiteId(ValueObject[UUID]):
    value: UUID
