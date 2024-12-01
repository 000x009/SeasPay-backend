from typing import Optional

from src.domain.value_objects.card_requisite import Number, Holder
from src.domain.value_objects.requisite import RequisiteId, RequisiteType, RequisiteTypeEnum


class CardRequisite:
    __slots__ = (
        "requisite_id",
        "type",
        "number",
        "holder",
    )

    def __init__(
        self,
        requisite_id: RequisiteId,
        number: Number,
        holder: Holder,
        type: Optional[RequisiteType] = None,
    ) -> None:
        self.requisite_id = requisite_id
        self.type = type
        self.number = number
        self.holder = holder

        if self.type is None:
            self.type = RequisiteType(RequisiteTypeEnum.CARD)
