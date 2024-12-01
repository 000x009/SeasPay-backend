from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import CardRequisiteDAL
from src.infrastructure.data.models import CardRequisiteModel
from src.domain.entity.card_requisite import CardRequisite
from src.domain.value_objects.requisite import RequisiteId
from src.domain.value_objects.card_requisite import Number, Holder


class CardRequisiteDALImpl(CardRequisiteDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, card_requisite: CardRequisite) -> CardRequisite:
        model = CardRequisiteModel(
            requisite_id=card_requisite.requisite_id.value,
            number=card_requisite.number.value,
            holder=card_requisite.holder.value,
        )
        self.session.add(model)

        return card_requisite

    async def get(self, requisite_id: RequisiteId) -> Optional[CardRequisite]:
        stmt = select(CardRequisiteModel).where(CardRequisiteModel.requisite_id == requisite_id.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return CardRequisite(
            requisite_id=RequisiteId(model.requisite_id),
            number=Number(model.number),
            holder=Holder(model.holder),
        )
