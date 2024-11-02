from typing import List

from src.application.common.uow import UoW
from src.application.common.dal.platform import PlatformDAL
from src.domain.value_objects.platform import PlatformID
from src.application.dto.platform import PlatformDTO, GetPlatformDTO, ListPlatformDTO


class PlatformService:
    def __init__(
        self,
        uow: UoW,
        platform_dal: PlatformDAL,
    ) -> None:
        self.uow = uow
        self.platform_dal = platform_dal

    async def get_platform(self, data: GetPlatformDTO) -> PlatformDTO:
        platform = await self.platform_dal.get(PlatformID(data.platform_id))

        return PlatformDTO(
            platform_id=platform.platform_id.value,
            name=platform.name.value,
            image_url=platform.image_url.value,
            web_place=platform.web_place.value,
            description=platform.description.value,
            login_data=platform.login_data.value,
        )

    async def list_platform(self, data: ListPlatformDTO) -> List[PlatformDTO]:
        platforms = await self.platform_dal.list_(
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )

        return [
            PlatformDTO(
                platform_id=platform.platform_id.value,
                name=platform.name.value,
                image_url=platform.image_url.value,
                web_place=platform.web_place.value,
                description=platform.description.value,
                login_data=platform.login_data.value,
            )
            for platform in platforms
        ]
