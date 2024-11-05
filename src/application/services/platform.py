from src.application.common.uow import UoW
from src.application.common.dal.platform import PlatformDAL
from src.domain.value_objects.platform import PlatformID
from src.application.dto.platform import (
    PlatformDTO,
    GetPlatformDTO,
    ListPlatformDTO,
    PlatformListResultDTO,
    DeletePlatformDTO,
    UpdatePlatformDTO,
    CreatePlatformDTO,
)
from src.domain.entity.platform import Platform
from src.domain.value_objects.platform import (
    WebPlace,
    Name,
    Description,
    ImageURL,
    LoginData,
)


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

    async def list_platform(self, data: ListPlatformDTO) -> PlatformListResultDTO:
        platforms = await self.platform_dal.list_(
            limit=data.pagination.limit,
            offset=data.pagination.offset,
        )
        total = await self.platform_dal.get_total()

        platforms = [
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

        return PlatformListResultDTO(
            platforms=platforms,
            total=total,
        )

    async def delete_platform(self, data: DeletePlatformDTO) -> None:
        await self.platform_dal.delete(PlatformID(data.platform_id))
        await self.uow.commit()

    async def update_platform(self, data: UpdatePlatformDTO) -> PlatformDTO:
        platform = await self.platform_dal.get(PlatformID(data.platform_id))
        platform.name = Name(data.name)
        platform.image_url = ImageURL(data.image_url)
        platform.web_place = WebPlace(data.web_place)
        platform.description = Description(data.description)
        platform.login_data = LoginData(data.login_data)

        updated_platform = await self.platform_dal.update(
            platform_id=PlatformID(data.platform_id),
            updated_platform=platform,
        )
        await self.uow.commit()

        return PlatformDTO(
            platform_id=updated_platform.platform_id.value,
            name=updated_platform.name.value,
            image_url=updated_platform.image_url.value,
            web_place=updated_platform.web_place.value,
            description=updated_platform.description.value,
            login_data=updated_platform.login_data.value,
        )

    async def create_platform(self, data: CreatePlatformDTO) -> PlatformDTO:
        platform = Platform(
            name=Name(data.name),
            image_url=ImageURL(data.image_url),
            description=Description(data.description),
            login_data=LoginData(data.login_data),
        )
        created_platform = await self.platform_dal.insert(platform)
        await self.uow.commit()

        return PlatformDTO(
            platform_id=created_platform.platform_id.value,
            name=created_platform.name.value,
            image_url=created_platform.image_url.value,
            web_place=created_platform.web_place.value,
            description=created_platform.description.value,
            login_data=created_platform.login_data.value,
        )
