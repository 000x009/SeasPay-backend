from src.application.common.dal import CryptoRequisiteDAL
from src.application.dto.crypto_requisite import CryptoRequisiteCreateDTO, GetCryptoRequisiteDTO, CryptoRequisiteDTO
from src.application.dto.requisite import CreateRequisiteDTO
from src.domain.entity.crypto_requisite import CryptoRequisite
from src.domain.value_objects.crypto_requisite import WalletAddress, Memo, Asset, Network
from src.domain.value_objects.requisite import RequisiteId, RequisiteTypeEnum
from src.application.services.requisite import RequisiteService
from src.application.common.uow import UoW


class CryptoRequisiteService:
    def __init__(
        self,
        dal: CryptoRequisiteDAL,
        requisite_service: RequisiteService,
        uow: UoW,
    ) -> None:
        self.dal = dal
        self.requisite_service = requisite_service
        self.uow = uow

    async def create(self, data: CryptoRequisiteCreateDTO) -> CryptoRequisiteDTO:
        requisite = await self.requisite_service.create(
            CreateRequisiteDTO(
                user_id=data.user_id,
                type=RequisiteTypeEnum.CRYPTO,
            )
        )
        crypto_requisite = await self.dal.insert(
            CryptoRequisite(
                requisite_id=RequisiteId(requisite.id),
                wallet_address=WalletAddress(data.wallet_address),
                memo=Memo(data.memo),
                asset=Asset(data.asset),
                network=Network(data.network),
            )
        )
        await self.uow.commit()

        return CryptoRequisiteDTO(
            requisite_id=crypto_requisite.requisite_id.value,
            wallet_address=crypto_requisite.wallet_address.value,
            memo=crypto_requisite.memo.value,
            asset=crypto_requisite.asset.value,
            network=crypto_requisite.network.value,
        )

    async def get_requisite(self, data: GetCryptoRequisiteDTO) -> CryptoRequisiteDTO:
        crypto_requisite = await self.dal.get(RequisiteId(data.requisite_id))

        return CryptoRequisiteDTO(
            requisite_id=crypto_requisite.requisite_id.value,
            wallet_address=crypto_requisite.wallet_address.value,
            memo=crypto_requisite.memo.value,
            asset=crypto_requisite.asset.value,
            network=crypto_requisite.network.value,
        )
