from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal.requisite import RequisiteDAL
from src.domain.entity.requisite import Requisite
from src.infrastructure.data.models import RequisiteModel
from src.domain.value_objects.requisite import RequisiteId, RequisiteType, CreatedAt
from src.domain.value_objects.user import UserID
from src.domain.value_objects.pagination import Limit, Offset


class RequisiteDALImpl(RequisiteDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, requisite: Requisite) -> Requisite:
        model = RequisiteModel(
            id=requisite.id.value,
            user_id=requisite.user_id.value,
            type=requisite.type.value.value,
            created_at=requisite.created_at.value,
        )
        self.session.add(model)

        return requisite

    async def get_one(self, requisite_id: RequisiteId) -> Optional[Requisite]:
        query = select(RequisiteModel).where(RequisiteModel.id == requisite_id.value)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return Requisite(
            id=RequisiteId(model.id),
            user_id=UserID(model.user_id),
            type=RequisiteType(model.type),
            created_at=CreatedAt(model.created_at),
        )
    
    async def list_by_user(
        self, user_id: UserID, limit: Limit, offset: Offset
    ) -> List[Requisite]:
        query = (
            select(RequisiteModel)
            .where(RequisiteModel.user_id == user_id.value)
            .order_by(RequisiteModel.created_at.desc())
            .limit(limit.value)
            .offset(offset.value)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()

        return [
            Requisite(
                id=RequisiteId(model.id),
                user_id=UserID(model.user_id),
                type=RequisiteType(model.type),
                created_at=CreatedAt(model.created_at),
            )
            for model in models
        ]

    async def get_user_total(self, user_id: UserID) -> Optional[int]:
        query = select(func.count(RequisiteModel.id)).where(RequisiteModel.user_id == user_id.value)
        result = await self.session.execute(query)
        total = result.scalar_one_or_none()

        return total
