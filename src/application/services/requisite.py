from src.application.common.dal.requisite import RequisiteDAL
from src.application.dto.requisite import (
    RequisiteListDTO,
    RequisiteListResultDTO,
    GetRequisiteDTO,
    RequisiteDTO,
    CreateRequisiteDTO,
)
from src.domain.value_objects.user import UserID
from src.domain.value_objects.pagination import Limit, Offset
from src.domain.value_objects.requisite import RequisiteId, RequisiteType
from src.domain.entity.requisite import Requisite
from src.domain.exceptions.requisite import RequisiteNotFound
from src.application.common.uow import UoW


class RequisiteService:
    def __init__(self, dal: RequisiteDAL, uow: UoW) -> None:
        self.dal = dal
        self.uow = uow

    async def list_requisites(self, data: RequisiteListDTO) -> RequisiteListResultDTO:
        requisites = await self.dal.list_by_user(
            user_id=UserID(data.user_id),
            limit=Limit(data.pagination.limit),
            offset=Offset(data.pagination.offset),
        )
        total = await self.dal.get_user_total(UserID(data.user_id))

        return RequisiteListResultDTO(
            requisites=[
                RequisiteDTO(
                    id=requisite.id.value,
                    user_id=requisite.user_id.value,
                    type=requisite.type.value,
                    created_at=requisite.created_at.value,
                )
                for requisite in requisites
            ],
            total=total,
        )

    async def get_requisite(self, data: GetRequisiteDTO) -> RequisiteDTO:
        requisite = await self.dal.get_one(RequisiteId(data.requisite_id))
        if not requisite:
            raise RequisiteNotFound(f"Requisite with id <{data.requisite_id}> not found")

        return RequisiteDTO(
            id=requisite.id.value,
            user_id=requisite.user_id.value,
            type=requisite.type.value,
            created_at=requisite.created_at.value,
        )

    async def create(self, data: CreateRequisiteDTO) -> RequisiteDTO:
        requisite = await self.dal.insert(
            Requisite(
                user_id=UserID(data.user_id),
                type=RequisiteType(data.type),
            )
        )
        await self.uow.commit()

        return RequisiteDTO(
            id=requisite.id.value,
            user_id=requisite.user_id.value,
            type=requisite.type.value,
            created_at=requisite.created_at.value,
        )
