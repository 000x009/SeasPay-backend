from dataclasses import dataclass, field

from src.domain.value_objects.requisite import RequisiteTypeEnum


@dataclass(frozen=True)
class CardRequisiteDTO:
    requisite_id: int
    number: str
    holder: str
    type: RequisiteTypeEnum = field(default=RequisiteTypeEnum.CARD)


@dataclass(frozen=True)
class CardRequisiteCreateDTO:
    user_id: int
    number: str
    holder: str


@dataclass(frozen=True)
class GetCardRequisiteDTO:
    requisite_id: int
