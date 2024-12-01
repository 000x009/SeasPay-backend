from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.dal import CryptoRequisiteDAL
from src.infrastructure.data.models import CryptoRequisiteModel
from src.domain.entity.crypto_requisite import CryptoRequisite
from src.domain.value_objects.requisite import RequisiteId
from src.domain.value_objects.crypto_requisite import WalletAddress, Network, Memo, Asset


class CryptoRequisiteDALImpl(CryptoRequisiteDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def insert(self, crypto_requisite: CryptoRequisite) -> CryptoRequisite:
        model = CryptoRequisiteModel(
            requisite_id=crypto_requisite.requisite_id.value,
            wallet_address=crypto_requisite.wallet_address.value,
            network=crypto_requisite.network.value,
            memo=crypto_requisite.memo.value,
            asset=crypto_requisite.asset.value,
        )
        self.session.add(model)

        return crypto_requisite

    async def get(self, requisite_id: RequisiteId) -> Optional[CryptoRequisite]:
        stmt = select(CryptoRequisiteModel).where(CryptoRequisiteModel.requisite_id == requisite_id.value)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return CryptoRequisite(
            requisite_id=RequisiteId(model.requisite_id),
            wallet_address=WalletAddress(model.wallet_address),
            network=Network(model.network),
            memo=Memo(model.memo),
            asset=Asset(model.asset),
        )
