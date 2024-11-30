from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update

from src.domain.value_objects.platform import (
    PlatformID,
    Name,
    Description,
    ImageURL,
    WebPlace,
    LoginData,
)
from src.domain.entity.platform import Platform, PlatformDB
from src.infrastructure.data.models import PlatformModel
from src.application.common.dal.platform import PlatformDAL


class PlatformDALImpl(PlatformDAL):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, platform_id: PlatformID) -> PlatformDB:
        query = select(PlatformModel).where(PlatformModel.id == platform_id.value)
        result = await self.session.execute(query)
        platform = result.scalar_one()

        return PlatformDB(
            platform_id=PlatformID(platform.id),
            name=Name(platform.name),
            image_url=ImageURL(platform.image_url),
            web_place=WebPlace(platform.web_place),
            description=Description(platform.description),
            login_data=LoginData(platform.login_data),
        )

    async def insert(self, platform: Platform) -> PlatformDB:
        platform_model = PlatformModel(
            name=platform.name.value,
            image_url=platform.image_url.value,
            description=platform.description.value,
            login_data=platform.login_data.value,
        )
        self.session.add(platform_model)

        return PlatformDB(
            platform_id=PlatformID(platform_model.id),
            name=Name(platform_model.name),
            image_url=ImageURL(platform_model.image_url),
            web_place=WebPlace(platform_model.web_place),
            description=Description(platform_model.description),
            login_data=LoginData(platform_model.login_data),
        )

    async def list_(self, limit: int, offset: int) -> List[PlatformDB]:
        query = (
            select(PlatformModel)
            .limit(limit)
            .offset(offset)
            .order_by(PlatformModel.web_place)
        )
        result = await self.session.execute(query)
        platforms = result.scalars().all()

        return [
            PlatformDB(
                platform_id=PlatformID(platform.id),
                name=Name(platform.name),
                image_url=ImageURL(platform.image_url),
                web_place=WebPlace(platform.web_place),
                description=Description(platform.description),
                login_data=LoginData(platform.login_data),
            )
            for platform in platforms
        ]

    async def get_total(self) -> Optional[int]:
        query = select(func.count(PlatformModel.id))
        result = await self.session.execute(query)
        total = result.scalar_one_or_none()

        return total

    async def delete(self, platform_id: PlatformID) -> None:
        query = delete(PlatformModel).where(PlatformModel.id == platform_id.value)
        await self.session.execute(query)

    async def update(
        self,
        platform_id: PlatformID,
        updated_platform: Platform,
    ) -> PlatformDB:
        platform_model = PlatformModel(
            id=platform_id.value,
            name=updated_platform.name.value,
            image_url=updated_platform.image_url.value,
            web_place=updated_platform.web_place.value,
            description=updated_platform.description.value,
            login_data=updated_platform.login_data.value,
        )
        await self.session.merge(platform_model)

        return PlatformDB(
            platform_id=PlatformID(platform_model.id),
            name=Name(platform_model.name),
            image_url=ImageURL(platform_model.image_url),
            web_place=WebPlace(platform_model.web_place),
            description=Description(platform_model.description),
            login_data=LoginData(platform_model.login_data),
        )
