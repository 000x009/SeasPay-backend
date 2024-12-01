from src.domain.value_objects.card_requisite import Number, Holder
from src.domain.value_objects.requisite import RequisiteId, RequisiteType


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
        type: RequisiteType,
        number: Number,
        holder: Holder,
    ) -> None:
        self.requisite_id = requisite_id
        self.type = type
        self.number = number
        self.holder = holder
