from src.application.common.dal import CardRequisiteDAL
from src.application.dto.card_requisite import CardRequisiteCreateDTO, GetCardRequisiteDTO, CardRequisiteDTO
from src.application.dto.requisite import CreateRequisiteDTO
from src.domain.entity.card_requisite import CardRequisite
from src.domain.value_objects.card_requisite import Number, Holder
from src.domain.value_objects.requisite import RequisiteId, RequisiteTypeEnum
from src.application.services.requisite import RequisiteService
from src.application.common.uow import UoW


class CardRequisiteService:
    def __init__(
        self,
        dal: CardRequisiteDAL,
        requisite_service: RequisiteService,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.requisite_service = requisite_service
        self.uow = uow

    async def create(self, data: CardRequisiteCreateDTO) -> CardRequisiteDTO:
        requisite = await self.requisite_service.create(
            CreateRequisiteDTO(
                user_id=data.user_id,
                type=RequisiteTypeEnum.CARD,
            )
        )
        card_requisite = await self.dal.insert(
            CardRequisite(
                requisite_id=RequisiteId(requisite.id),
                number=Number(data.number),
                holder=Holder(data.holder),
            )
        )
        await self.uow.commit()

        return CardRequisiteDTO(
            requisite_id=card_requisite.requisite_id.value,
            number=card_requisite.number.value,
            holder=card_requisite.holder.value,
        )

    async def get_requisite(self, data: GetCardRequisiteDTO) -> CardRequisiteDTO:
        card_requisite = await self.dal.get(RequisiteId(data.requisite_id))

        return CardRequisiteDTO(
            requisite_id=card_requisite.requisite_id.value,
            number=card_requisite.number.value,
            holder=card_requisite.holder.value,
        )
